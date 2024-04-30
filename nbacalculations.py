import sqlite3
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect('complete.db')
cur = conn.cursor()

def get_salary_avg(cur):
    cur.execute("SELECT AVG(salary) FROM players")
    avg = cur.fetchone()[0] 
    return avg

def get_weight_avg(cur):
    cur.execute("SELECT AVG(weight_id) FROM players")
    avg_weight = cur.fetchone()[0]
    return avg_weight

def get_height_avg(cur):
    cur.execute("SELECT AVG(height_id) FROM players")
    avg_height = cur.fetchone()[0]
    return avg_height

def get_avg_experience(cur):
    cur.execute("SELECT AVG(experience) FROM players")
    avg_experience = cur.fetchone()[0]
    return avg_experience

def get_avg_dco(cur):
    cur.execute("SELECT AVG(depthchartorder) FROM players")
    avg_dco = cur.fetchone()[0]
    return avg_dco



def main():
    cur = conn.cursor()
    
    average_salary = get_salary_avg(cur)
    average_weight = get_weight_avg(cur)
    average_height = get_height_avg(cur)
    average_experience = get_avg_experience(cur)
    average_depth_chart_order = get_avg_dco(cur)



    cur.close()

   
if __name__ == "__main__":
    main()