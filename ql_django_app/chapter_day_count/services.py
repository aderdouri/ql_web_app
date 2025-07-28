import QuantLib as ql
from datetime import date, timedelta

def analyze_day_count_convention(convention_str: str, d1_py: date, d2_py: date):
    """
    Analyse le comportement d'une convention de décompte de jours choisie par l'utilisateur.
    Le graphique est maintenant basé sur la plage de dates de l'utilisateur.
    """
    
    d1 = ql.Date(d1_py.day, d1_py.month, d1_py.year)
    d2 = ql.Date(d2_py.day, d2_py.month, d2_py.year)
    
    day_counter = None
    if convention_str == 'Thirty360':
        day_counter = ql.Thirty360(ql.Thirty360.USA)
    elif convention_str == 'ActualActual':
        day_counter = ql.ActualActual(ql.ActualActual.ISMA)
    else:
        day_counter = ql.Actual365Fixed()

    # Calcul de la fraction d'année (inchangé)
    year_fraction = 0.0
    try:
        year_fraction = day_counter.yearFraction(d1, d2)
    except Exception:
        try:
            year_fraction = day_counter.yearFraction(d1, d2, d1, d2)
        except Exception as e:
            print(f"Could not calculate year fraction: {e}")

    # Détection de l'anomalie (inchangé)
    anomaly_result = None
    if convention_str == 'Thirty360':
        calendar = ql.TARGET()
        last_day_of_month = calendar.endOfMonth(d1)
        day_before_last = last_day_of_month - 1
        if day_before_last.dayOfMonth() == 30 and last_day_of_month.dayOfMonth() == 31:
             if day_counter.yearFraction(day_before_last, last_day_of_month) == 0.0:
                 anomaly_result = "Anomaly Detected! The fraction between the 30th and 31st of this month is 0.0."
        

    plot_points = []
    start_date_plot = d1  # Commence à la 'Start Date' de l'utilisateur
    end_date_plot = d2    # Se termine à la 'End Date' de l'utilisateur
    
    # On s'assure que la plage n'est pas trop grande pour ne pas surcharger le navigateur
    if (end_date_plot - start_date_plot) > (365 * 10): # Limite de 10 ans
        end_date_plot = start_date_plot + ql.Period(10, ql.Years)

    dates_for_plot = [start_date_plot + i for i in range(end_date_plot - start_date_plot + 1)]
    
    try:
        if convention_str == 'ActualActual':
            times = [day_counter.yearFraction(start_date_plot, d, start_date_plot, end_date_plot) for d in dates_for_plot]
        else:
            times = [day_counter.yearFraction(start_date_plot, d) for d in dates_for_plot]
        
        plot_points = [{'x': dt.ISO(), 'y': t} for dt, t in zip(dates_for_plot, times)]
    except Exception as e:
        print(f"Could not generate plot points: {e}")

    return {
        'year_fraction': round(year_fraction, 8),
        'anomaly': anomaly_result,
        'plot_points': plot_points
    }