"""Hydraulic calculations and utilities.
"""
import math 

def mannings_discharge(n, area, hydraulic_radius, slope):
    """Calculate discharge using Manning's equation.

    Args:
        n (float): Manning's roughness coefficient.
        area (float): Cross-sectional area of flow (m^2).
        hydraulic_radius (float): Hydraulic radius (m).
        slope (float): Slope of the energy grade line (m/m).

    Returns:
        float: Discharge (m^3/s).
    """
    discharge = (1 / n) * area * (hydraulic_radius ** (2/3)) * (slope ** 0.5)
    return discharge

def hazen_williams_headloss(Q, C, D, L):
    """
    Hazen-Williams head loss.
    
    Parameters:
        Q (float): Discharge (m³/s)
        C (float): Hazen-Williams coefficient
        D (float): Pipe diameter (m)
        L (float): Length of pipe (m)

    Returns:
        hL (float): Head loss (m)
    """
    return 10.67 * (L * (Q ** 1.852)) / ((C ** 1.852) * (D ** 4.87))

def darcy_weisbach_headloss(f, L, D, V, g=9.81):
    """
    Darcy-Weisbach head loss: hL = f * (L/D) * (V² / 2g)
    
    Parameters:
        f (float): friction factor
        L (float): length of pipe (m)
        D (float): diameter (m)
        V (float): flow velocity (m/s)
        g (float): gravity (m/s²)
        
    Returns:
        hL (float): head loss (m)
    """
    return f * (L/D) * (V**2 / (2*g))

def open_channel_flow(A, V):
    """
    Continuity equation for open channels: Q = A * V
    
    Parameters:
        A (float): flow area (m²)
        V (float): velocity (m/s)

    Returns:
        Q (float): discharge (m³/s)
    """
    return A * V

def culvert_size(Q, n, S):
    """
    Estimates culvert diameter (m) for given flow using full-flow Manning’s equation.
    
    Parameters:
        Q (float): target flow (m³/s)
        n (float): Manning roughness
        S (float): slope (m/m)
    
    Returns:
        D (float): culvert diameter (m)
    """
    # Solve iteratively: Q = (1/n) * A * R^(2/3) * S^0.5
    D = 0.1  # start with 100 mm guess
    
    for _ in range(100000):
        A = math.pi * D**2 / 4
        R = D / 4  # hydraulic radius for full circular pipe
        Q_est = mannings_discharge(n, A, R, S)
        
        # adjust diameter
        D += 0.0001 * (Q - Q_est)

        if abs(Q - Q_est) < 0.000001:
            break

    return round(D, 4)


