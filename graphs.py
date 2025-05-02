import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def render_city_of_residence_plot():
    conn = None
    try:
        conn = sqlite3.connect('instance/users.db')
        query = "SELECT * FROM entry"
        df = pd.read_sql(query, conn)
        city_of_residence_df = df.groupby('city_of_residence').count().sort_values('age', ascending=False)
        ax1 = plt.gca()
        ax1.bar(city_of_residence_df.index, city_of_residence_df.age, color="blue", linewidth=.2, width=.2)
        ax1.set_xlabel('city of residence')
        plt.xticks(fontsize=10, rotation=90, color='black')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('static/images/residence_light.png', transparent=True)

        #dark mode
        plt.xticks(color='white')
        plt.yticks(color='white')
        ax1.set_xlabel('city of residence', color='white')
        plt.grid(True, color='black')
        plt.savefig('static/images/residence_dark.png', transparent=True)

    except sqlite3.Error as e:
        return f"Database Error: {e}", 500
    finally:
        if conn:
            conn.close()