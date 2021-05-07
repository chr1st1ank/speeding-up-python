
function merge(l, r)
    result = Int64[]
    
    while !(isempty(l) || isempty(r))
        if l[1] <= r[1]
            push!(result, popfirst!(l))
        else
            push!(result, popfirst!(r))
        end
    end
    
    while !isempty(l)
        push!(result, popfirst!(l))
    end
    
    while !isempty(r)
        push!(result, popfirst!(r))
    end
    
    return result
end

function mergesort(l)
    i = 0
    if i > 20
        return
    end
    i += 1
    if size(l, 1) <= 1
        return l
    end
    part = div(size(l, 1), 2)
    left = mergesort(l[1:part])
    right = mergesort(l[part+1:size(l, 1)])
    return merge(left, right)
end
