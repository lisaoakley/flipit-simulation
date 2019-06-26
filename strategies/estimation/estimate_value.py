
def loss(current_estimate,future_val,gamma,alpha,reward):
    return current_estimate + alpha*(reward - current_estimate)

def future(current_estimate,future_val,gamma,alpha,reward):
    return current_estimate + alpha*(reward + gamma*future_val)

def td(current_estimate,future_val,gamma,alpha,reward):
    return current_estimate + alpha*(reward - current_estimate + gamma*future_val)