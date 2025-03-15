# Placement Eligibility App using Streamlit
# Libraries used -> Streamlit, Pandas, mysql connector
# Methodology used: Functions
# try...except block to identify the connectivity issues


import streamlit as st
import pandas as pd
import mysql.connector

#Database Configuration/Credentials to connect to "plcmnt" database 
# data type used -> dictionary (dict{})
db_config_det = {
    'host':'localhost',
    'user':'root',
    'password':'893107',
    'database':'plcmnt'
}

# Connecting to the database defined inside a function by passing the dictionary values that are user-defined
def connectdb_exec(query,db_config_det,params=None):
    connection=None
    cursor=None
    try:
        connection=mysql.connector.connect(**db_config_det)
        cursor=connection.cursor()
        cursor.execute(query,params)
        data=cursor.fetchall()
        return data
    except mysql.connector.Error as err:
        st.error(f"Error in executing the query:{err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# streamlit app interface
st.set_page_config(page_title="Placement Eligibility App", layout="centered") #defining the page name in the URL
st.title("Placement Eligibility App :rocket:") # defining the title of the page

# Criteria dropdown/ Criteria Selection
criteria = st.selectbox("Select Criteria:",[
    "Placement Eligible Students(Overall Excellence)",
    "Students placed with higher package",
    "Average Performing Students",
    "Programming Language that secured most placements",
    "Super Performer in Each Batch",
    "Students with consistent performance",
    "Student with highest project score and mini projects submission",
    "Number of placements by internship count in each Batch",
    "Mock Interview Score Distribution",
    "Batch-wise Placement Percentage"
    ])

#Queries for the Criterions listed:
if criteria:
    data = None
    if criteria == "Placement Eligible Students(Overall Excellence)":  
        n=st.slider("select number of students to display:", min_value = 1,max_value = 20,value=10)
        st.write(f"**Please find the list of candidates for the selected Criteria:**,{criteria}")
        query = """
                    select s.student_id, s.name, p.problems_solved, p.latest_project_score,
                    (ss.communication + ss.teamwork + ss.presentation)/3 as ss_avg,
                    pl.mock_interview_score
                    from Students s, Programming p, soft_skills ss, placements pl
                    where s.student_id = p.student_id and
                    s.student_id = ss.student_id and
                    s.student_id = pl.student_id
                    and pl.placement_status = 'Ready'
                    order by p.problems_solved desc, p.latest_project_score desc, ss_avg desc, pl.mock_interview_score desc
                    limit %s
                """
        data = connectdb_exec(query,db_config_det,(n,))
    elif criteria == "Students placed with higher package":
        n=st.slider("select number of students to display:", min_value = 1,max_value = 20,value=10)
        st.write(f"**Please find the list of candidates for the selected Criteria:**,{criteria}")
        query="""
                 select s.student_id, s.name, pl.company_name, pl.placement_package
                 from Students s, Placements pl
                 where s.student_id = pl.student_id and
                 pl.placement_status in ('Placed','Awaiting Offer')
                 order by pl.placement_package desc
                 limit %s
            """
        data = connectdb_exec(query,db_config_det,(n,))
    elif criteria == "Average Performing Students":
        problems_threshold = st.slider("Select the number of Problems Solved:", min_value=0, max_value=450, value=50)
        ss_threshold = st.slider("Select the average threshold:", min_value=0,max_value=100,value=70)
        n=st.slider("select number of students to display:", min_value = 1,max_value = 20,value=10)
        st.write(f"**Please find the list of candidates for the selected Criteria:**,{criteria}")
        query = """
                select s.student_id, s.name, p.problems_solved,
                (ss.communication + ss.teamwork + ss.presentation) / 3 AS avg_soft_skills
                from Students s, Programming p, Soft_Skills ss where
                s.student_id = p.student_id and
                s.student_id = ss.student_id and
                (p.problems_solved < %s  
                and (ss.communication + ss.teamwork + ss.presentation) / 3 < %s)
                order by p.problems_solved desc
                limit %s
            """
        data = connectdb_exec(query,db_config_det,(problems_threshold,ss_threshold,n,))
    elif criteria == "Programming Language that secured most placements":
        query = """
                select p.language, count(*) as placement_count
                from Programming p, Placements pl
                where p.student_id = pl.student_id
                and pl.placement_status in ('Placed','Awaiting Offer')
                group by p.language
                order by placement_count desc
                """
        data = connectdb_exec(query,db_config_det)
    elif criteria == "Super Performer in Each Batch":
        query = """
                select s.student_id, s.name, s.course_batch, p.problems_solved,p.latest_project_score,
                (ss.communication + ss.teamwork + ss.presentation)/3 as avg_soft_skills,
                pl.mock_interview_score 
                from Students s
                join Programming p on s.student_id = p.student_id 
                join Soft_skills ss on s.student_id = ss.student_id 
                join Placements pl on s.student_id = pl.student_id 
                where pl.placement_status = 'Ready' and 
                (p.problems_solved + p.latest_project_score + ((ss.communication + ss.teamwork + ss.presentation)/3) + pl.mock_interview_score) =
                (select max(problems_solved + latest_project_score + (communication+teamwork+presentation)/3 + mock_interview_score) 
                from Students s2
                join Programming p2 on s2.student_id = p2.student_id 
                join Soft_skills ss2 on s2.student_id = ss2.student_id 
                join Placements pl2 on s2.student_id = pl2.student_id 
                where pl2.placement_status = 'Ready' and 
                s2.course_batch = s.course_batch
                )
                order by s.course_batch
                """
        data = connectdb_exec(query,db_config_det)
    elif criteria == "Students with consistent performance":
        n=st.slider("select number of students to display:", min_value = 1,max_value = 20,value=10)
        st.write(f"**Please find the list of candidates for the selected Criteria:**,{criteria}")
        query = """
                select s.student_id, s.name, avg(p.problems_solved) as avg_problems_solved,
                avg(p.latest_project_score) as avg_project_score
                from Students s, Programming p
                where s.student_id = p.student_id
                group by s.student_id, s.name
                order by avg(p.problems_solved) desc, avg(p.latest_project_score) desc
                limit %s
                """
        data = connectdb_exec(query,db_config_det,(n,))
    elif criteria == "Student with highest project score and mini projects submission":
        n=st.slider("select number of students to display:", min_value = 1,max_value = 20,value=10)
        st.write(f"**Please find the list of candidates for the selected Criteria:**,{criteria}")
        query = """
                select s.student_id, s.name, p.latest_project_score, p.mini_projects
                from Students s, Programming p
                where s.student_id = p.student_id
                order by p.latest_project_score desc, p.mini_projects desc
                limit %s;
                """
        data = connectdb_exec(query,db_config_det,(n,))
    elif criteria == "Number of placements by internship count in each Batch":
        query = """
                select s.student_id, s.name, pl.placement_status, sum(pl.internships_completed)
                from  Students s, Placements pl
                where s.student_id = pl.student_id
                and pl.placement_status in ('Placed','Awaiting Offer')
                group by s.student_id, s.name, placement_status
                order by sum(pl.internships_completed) desc;
                """
        data = connectdb_exec(query,db_config_det)
    elif criteria == "Mock Interview Score Distribution":
        query = """
                select s.student_id, s.name, pl.mock_interview_score, pl.placement_status
                from Placements pl, Students s
                where s.student_id = pl.student_id
                group by s.student_id, s.name, pl.mock_interview_score, pl.placement_status
                order by pl.mock_interview_score desc
                """
        data = connectdb_exec(query,db_config_det)
    elif criteria == "Batch-wise Placement Percentage":
        query = """
                select
                s.course_batch,
                COUNT(CASE WHEN pl.placement_status IN ('Placed', 'Awaiting Offer') THEN 1 ELSE NULL END) AS placed_count,
                (SELECT COUNT(*) FROM Students WHERE course_batch = s.course_batch) AS total_count,
                (COUNT(CASE WHEN pl.placement_status IN ('Placed', 'Awaiting Offer') THEN 1 ELSE NULL END) / 
                (SELECT COUNT(*) FROM Students WHERE course_batch = s.course_batch)) * 100 AS placement_percentage
                from Students s, Placements pl
                where s.student_id = pl.student_id
                group by s.course_batch
                """
        data = connectdb_exec(query,db_config_det)
# Result display
# Methodology used : Storing the results in dataframe
    if data is not None:
        if criteria == "  Placement Eligible Students(Overall Excellence)":
            df=pd.DataFrame(data,columns=["Student ID","Name","Problems Solved","Latest Prj Score","SoftSkillsAvg","Mock Inv Score"])
        elif criteria == "Students placed with higher package":
            df=pd.DataFrame(data,columns=["Student ID","Name","Company Name","Placement Package"])
        elif criteria == "Average Performing Students":
            df=pd.DataFrame(data,columns=["Student ID","Name","Problems Solved","Avg Soft Skills"])
        elif criteria == "Programming Language that secured most placements":
            df=pd.DataFrame(data,columns=["Language","Placement_Count"])
        elif criteria == "Super Performer in Each Batch":
            df=pd.DataFrame(data,columns=["Student ID","Name","Batch","Problems Solved","Latest Prj Score","Avg Soft Skills","Mock Interview Score"])
        elif criteria == "Students with consistent performance":
            df=pd.DataFrame(data,columns=["Student ID","Name","Avg Problems Solved","Avg Project Score"])
        elif criteria == "Student with highest project score and mini projects submission":
            df=pd.DataFrame(data,columns=["Student ID","Name","Latest Prj Score","Mini Projects Submitted"])
        elif criteria == "Number of placements by internship count in each Batch":
            df=pd.DataFrame(data,columns=["Student ID","Student Name","Placement Status","Internships Completed"])
        elif criteria == "Mock Interview Score Distribution":
            df=pd.DataFrame(data,columns=["Student ID","Student Name","Mock Interview Score","Placement Status"])
        elif criteria == "Batch-wise Placement Percentage":
            df=pd.DataFrame(data,columns=["Batch","Placed Count","Total Count","Placement %"])
        else:
            df=pd.DataFrame(data)
        st.dataframe(df.style.highlight_max(axis=0))
    else:
        st.info("No Students match this criteria or an error occured.")
else:
    st.info("Please select valid criteria")
