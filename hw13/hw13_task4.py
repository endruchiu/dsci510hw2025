
import sqlite3

def get_artists_by_genre(genre='Rock'):
    """Return a list of artist names for a given genre.
    
    Args:
        genre (str): The genre to filter artists by (default: 'Rock')
    
    Returns:
        list: List of artist names (strings)
    """
    conn = sqlite3.connect('music_festival.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM artists WHERE genre = ?", (genre,))
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

def get_total_revenue():
    """Calculate the total revenue from ticket sales.
    
    Returns:
        float: Total revenue from all tickets
    """
    conn = sqlite3.connect('music_festival.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(price) FROM tickets")
    result = cursor.fetchone()[0] or 0.0
    conn.close()
    return result

def get_performances_per_stage():
    """Count the number of performances per stage.
    
    Returns:
        list: List of tuples (stage name, performance count)
    """
    conn = sqlite3.connect('music_festival.db')
    cursor = conn.cursor()
    cursor.execute("SELECT s.name, COUNT(p.performance_id) as performance_count FROM stages s LEFT JOIN performances p ON s.stage_id = p.stage_id GROUP BY s.stage_id, s.name")
    results = cursor.fetchall()
    conn.close()
    return results

def get_performances_by_date(date='2023-07-04'):
    """List all performances on a given date with artist names and stage locations.
    
    Args:
        date (str): The date to filter performances by (default: '2023-07-04')
    
    Returns:
        list: List of tuples (artist name, location, start time, end time)
    """
    conn = sqlite3.connect('music_festival.db')
    cursor = conn.cursor()
    cursor.execute("SELECT a.name, s.location, p.start_time, p.end_time FROM performances p JOIN artists a ON p.artist_id = a.artist_id JOIN stages s ON p.stage_id = s.stage_id WHERE DATE(p.start_time) = ?", (date,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_artists_with_long_performances(hours=2):
    """Identify artists with performances longer than a given duration.
    
    Args:
        hours (float): Minimum performance duration in hours (default: 2)
    
    Returns:
        list: List of artist names (strings) with performances > hours
    """
    conn = sqlite3.connect('music_festival.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT a.name FROM artists a JOIN performances p ON a.artist_id = p.artist_id WHERE (JULIANDAY(p.end_time) - JULIANDAY(p.start_time)) * 24 > ?", (hours,))
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

if __name__ == '__main__':
    print("Rock artists:", get_artists_by_genre())
    print("Total revenue:", get_total_revenue())
    print("Performances per stage:", get_performances_per_stage())
    print("Performances on 2023-07-04:", get_performances_by_date())
    print("Artists with >2 hour performances:", get_artists_with_long_performances())
