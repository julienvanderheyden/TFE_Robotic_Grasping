function rotor_to_matrix(R)
    s, (x, y, z) = R.scalar, R.bivector 
    
    return [
        1 - 2(y^2 + z^2)   2(x*y - s*z)   2(x*z + s*y)
        2(x*y + s*z)   1 - 2(x^2 + z^2)   2(y*z - s*x)
        2(x*z - s*y)   2(y*z + s*x)   1 - 2(x^2 + y^2)
    ]
end

function struct_fields_and_types(T::Type)
    for (name, type) in zip(fieldnames(T), fieldtypes(T))
        println(name, "::", type)
    end
end



function generate_q_init(vms_compiled; ff=false, mf=false, rf=false, lf=false)
    q_init = zero_q(vms_compiled.robot)

    if ff
        q_init[3] = 1.4
        q_init[4] = 1.57
        q_init[5] = 1.57
    end

    if mf
        q_init[8] = 1.4
        q_init[9] = 1.57
        q_init[10] = 1.57
    end

    if rf
        q_init[12] = 1.4
        q_init[13] = 1.57
        q_init[14] = 1.57
    end

    if lf
        q_init[17] = 1.4
        q_init[18] = 1.57
        q_init[19] = 1.57
    end

    return q_init
end

function generate_stiffnesses_linear_scaling(base::Float64, alpha::Float64, beta::Float64)
    num_fingers = 5  # little to thumb
    num_phalanges = 3  # distal to proximal

    stiffnesses = Float64[]

    for finger in 0:num_fingers-1
        for phalanx in 0:num_phalanges-1
            # Scale factors normalized in [0, 1]
            finger_scale = finger / (num_fingers - 1)   # from 0 (little) to 1 (thumb)
            phalanx_scale = phalanx / (num_phalanges - 1)  # from 0 (distal) to 1 (proximal)

            stiffness = base * (1 + alpha * phalanx_scale) * (1 + beta * finger_scale)
            push!(stiffnesses, max(stiffness, 0.0))  # Ensure non-negative stiffness
        end
    end

    return stiffnesses
end

function generate_stiffnesses_geometric_scaling(base::Float64, alpha::Float64, beta::Float64)
    num_fingers = 5  # little to thumb
    num_phalanges = 3  # distal to proximal

    stiffnesses = Float64[]

    for finger in 0:num_fingers-1
        for phalanx in 0:num_phalanges-1
            # Scale factors normalized in [0, 1]
            finger_scale  = finger / (num_fingers - 1) # from 0 (little) to 1 (thumb)
            phalanx_scale = phalanx / (num_phalanges - 1) # from 0 (distal) to 1 (proximal)

            phalanx_factor = alpha^phalanx_scale     # from 1 to alpha
            finger_factor  = beta^finger_scale      # from 1 to beta

            stiffness = base * phalanx_factor * finger_factor
            push!(stiffnesses, stiffness)
        end
    end

    return stiffnesses
end

function circle_center_tangent_to_lines(p11, p12, p21, p22, r)

    p11 = Vector{Float64}(p11)
    p12 = Vector{Float64}(p12)
    p21 = Vector{Float64}(p21)
    p22 = Vector{Float64}(p22)

    d1 = p12 - p11
    d2 = p22 - p21

    A = hcat(d1, -d2)
    b = p21 - p11
    if rank(A) < 2
        error("Lines are parallel or coincident")
    end
    ts = A \ b
    P = p11 + ts[1] * d1  # Intersection point


    d1 = normalize(p12 - P)
    d2 = normalize(p22 - P)

    bisector = normalize(d1 + d2)

    cosθ = clamp(dot(d1, d2), -1.0, 1.0)
    θ = acos(cosθ)

    d = r / sin(θ / 2)

    C = P + d * bisector

    return C
end
