from astropy.time import Time
from astropy.coordinates import get_body, AltAz
import astropy.units as u
from datetime import datetime

def get_star_position(commit_date, user_lat=0, user_lon=0):
    """Convert commit timestamp to celestial coordinates"""
    # Convert commit time to astropy Time object
    t = Time(commit_date)
    
    # Get Moon position (or any celestial body)
    moon = get_body('moon', t, location=(user_lat*u.deg, user_lon*u.deg))
    
    # Convert to horizontal coordinate system
    altaz = moon.transform_to(AltAz(obstime=t, location=(user_lat*u.deg, user_lon*u.deg)))
    
    return {
        'ra': moon.ra.deg % 360,  # Right ascension
        'dec': moon.dec.deg,       # Declination
        'alt': altaz.alt.deg,      # Altitude
        'az': altaz.az.deg         # Azimuth
    }

def generate_constellation(commits):
    """Create real star positions based on commit times"""
    stars = []
    for commit in commits:
        commit_time = datetime.fromisoformat(commit['time'].replace('Z', '+00:00'))
        pos = get_star_position(commit_time)
        
        stars.append({
            'x': pos['ra'] / 36,         # Scale RA to 0-10
            'y': pos['dec'] / 9,         # Scale Dec to -10 to +10
            'size': commit['lines']**0.5,# Non-linear size scaling
            'color': time_to_color(commit_time),
            'message': commit['message'][:50]  # Truncate message
        })
    return stars

def time_to_color(dt):
    """Convert commit time to HSL color"""
    hue = dt.hour * 15  # 24h → 360°
    saturation = 70 + (dt.minute % 30)
    lightness = 40 + (dt.second % 20)
    return f'hsl({hue}, {saturation}%, {lightness}%)'
