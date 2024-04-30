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

def get_corr_exp_dco(cur):
    cur.execute("SELECT depthchartorder, experience FROM players WHERE depthchartorder IS NOT NULL AND experience IS NOT NULL")
    data = cur.fetchall()

    depthchartorder = []
    experience = []
    for row in data:
        depthchartorder.append(row[0])
        experience.append(row[1])

    corr_coef = np.corrcoef(depthchartorder, experience)[0, 1]
    return corr_coef
def get_sal_exp_corr(cur):
    cur.execute("SELECT salary, experience FROM players  WHERE experience IS NOT NULL")
    data = cur.fetchall()

    salary = []
    experience = []
    for row in data:
        salary.append(row[0])
        experience.append(row[1])

    corr_coef = np.corrcoef(salary, experience)[0, 1]
    return corr_coef

def exp_vs_sal(cur):
    cur.execute("SELECT experience, salary FROM players WHERE experience IS NOT NULL AND salary IS NOT NULL")
    data = cur.fetchall()
    experience = []
    salary = []
    for row in data:
        experience.append(row[0])
        salary.append(row[1])
    avg_experience = get_avg_experience(cur)
    slope, intercept = np.polyfit(experience, salary, 1)
    regression_line = [slope * x + intercept for x in experience]
    plt.scatter(experience, salary, color='pink', label= 'Data')
    plt.plot(experience, regression_line, color='magenta', label='Regression Line')
    plt.scatter(avg_experience, np.mean(salary), color='red', label='Average', marker='x', s=100)
    plt.title('Average Experience vs Salary')
    plt.xlabel('Experience')
    plt.ylabel('Salary')
    plt.show()

def salarygraph(cur):
    cur.execute("SELECT salary FROM players WHERE salary IS NOT NULL")
    data = cur.fetchall()
    salaries = []
    for row in data:
        salaries.append(row[0])
    plt.figure(figsize=(10, 6))  
    plt.bar(range(len(salaries)), salaries, color='orange', edgecolor='gray')
    plt.title('Salary Distribution')
    plt.xlabel('Player')
    plt.ylabel('Salary')
    plt.show()

   


def main():
    cur = conn.cursor()
    
    average_salary = get_salary_avg(cur)
    average_weight = get_weight_avg(cur)
    average_height = get_height_avg(cur)
    average_experience = get_avg_experience(cur)
    average_depth_chart_order = get_avg_dco(cur)
    correlation_salary_experience = get_sal_exp_corr(cur)
    correlation_depth_order_experience = get_corr_exp_dco(cur)
    exp_vs_sal(cur)
    salarygraph(cur)



    cur.close()
    conn.close()

   
if __name__ == "__main__":
    main()