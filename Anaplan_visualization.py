
import streamlit as st
def get_openai_response(prompt):
    from openai import OpenAI
    try:
        client = OpenAI(
          api_key = st.secrets["openAi_API_Key_visual"],
          BaseURL = st.secrets["BaseURL"],
          )
        
        
        completion = client.chat.completions.create(
          model="Meta-Llama-3.3-70B-Instruct-Turbo",
        #   model = "gpt-4o",
          messages=[
            {"role": "developer", "content": "SQL Developer and a data analyst"},
            {"role": "user", "content": prompt}
          ]
        )
        
        return completion.choices[0].message.content
    except:
        return "Too Frequent Submissions, Please try again in 60 seconds."
    
    
    
    
    


def get_response(user_input,prev_messages,db,schema):
    import streamlit as st
    
    
    prompt = f"""
    You are an AI assistant that converts user queries into SQL queries based on the given database schema.
    
    write a query for this User input: "{user_input}" based ont he schema below
    Schema:
    {schema}
    
    
    
    Instructions:
    - Generate only the SQL query based on the schema.
    -we want small output from the sql so try getting presize and less amount pf data so write query accordingly 
    - If the user asks for a graph, chart, or visualization, ignore the request and return only an SQL query that retrieves relevant data.
    - Do NOT include explanations, descriptions, or formatting.
    - Do NOT mention graphs, charts, or any kind of visualization.
    - The response must contain only the SQL query in plain text.
    
    Example:
    User Query: "How many employees work in the IT department?"
    Output: SELECT COUNT(*) FROM Employees WHERE Department = 'IT';
    
    User Query: "Give graph for sales distribution"
    Output: SELECT Month, Sales FROM SalesTable;
    
    Now, generate the SQL query for the given user input.
    """

    sql_query = get_openai_response(prompt)
    if sql_query == "Try after 1 min":
        # st.write("exception!!")
        return ""Too Frequent Submissions, Please try again in 60 seconds.""
    print(sql_query)
    text_table_data = db.run(sql_query)
    # st.write(text_table_data)

    graph_prompt = f'''
    Role : You are a data analyst in a company.
    Task: I will provide an SQL data table along with a user query. Based on the data, generate a structured dictionary output in the specified format (output should not have anything exept that output in text format).
    User Query: {user_input}
    sql query :{sql_query}
    SQL Query Output (Table Format):
    {text_table_data}
    
    Output Requirements:
    - Convert the given SQL table into a dictionary format.
    - Identify appropriate visualizations (choose from: "Line Plot", "Scatter Plot", "Bar Chart", "Histogram", "Pie Chart", "Box Plot", "Area Plot", "Stem Plot", "Heatmap", "Stack Plot", "Error Bar Plot", "Step Plot", "Quiver Plot", "Contour Plot", "Hexbin Plot").
    - Define x-axis and y-axis labels.
    - Include a Boolean field (`possible`) indicating whether a meaningful visualization can be generated or it should be numeeric 1 or 0.
    - length of both arrays in data should be equal and data whould have exactly 2 arrays (neither less nor more) so we can make graph simple
    
    Example Output Format:
    {{
        "data": {{
            "Category": ["Electronics", "Clothing", "Groceries", "Furniture", "Books"],
            "Sales": [300, 150, 400, 100, 200]
        }},
        "visualization": "Bar Chart",
        "xAxis_label": "Category",
        "x_Scale" :
        "yAxis_label": "Sales",
        "possible": 1
    }}
    
    
    Output Rules:
    - Return only the dictionary as plain text (no additional explanations or formatting).
    - Ensure the `visualization` field is a string format.
    - If visualization is not possible, set "possible": 0.
    '''



    text_dict = get_openai_response(graph_prompt)
    if text_dict == "Too Frequent Submissions, Please try again in 60 seconds.":
        return "Too Frequent Submissions, Please try again in 60 seconds."
    # st.write("----------------------------")
    # st.write(text_dict)
    # Convert string to dictionary
    import json

    data_dict_obj = json.loads(text_dict)
    # print(data_dict_obj)
    # print(data_dict_obj)



    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    if data_dict_obj["possible"]:
        # Extract data
        Normalize = min(len(data_dict_obj["data"][list(data_dict_obj["data"].keys())[0]]),len(data_dict_obj["data"][list(data_dict_obj["data"].keys())[1]]))
        data_dict_obj["data"][list(data_dict_obj["data"].keys())[0]] = data_dict_obj["data"][list(data_dict_obj["data"].keys())[0]][0:Normalize]
        data_dict_obj["data"][list(data_dict_obj["data"].keys())[1]] = data_dict_obj["data"][list(data_dict_obj["data"].keys())[1]][0:Normalize]
        # st.write(data_dict_obj["data"][list(data_dict_obj["data"].keys())[0]])
        main_data_dict = data_dict_obj["data"]
        df = pd.DataFrame(main_data_dict)
    
        # Extract column names for X and Y axes
        x_data = main_data_dict[list(main_data_dict.keys())[0]]
        y_data = main_data_dict[list(main_data_dict.keys())[1]]
        
    
        # Define the visualization type
        plot_type = data_dict_obj["visualization"]
    
        # Create the figure
        fig, ax = plt.subplots(figsize=(10, 5))

    # Dynamic Plot Selection
        if plot_type == "Line Plot":
            ax.plot(x_data, y_data, marker='o', linestyle='-', color='b')
        elif plot_type == "Scatter Plot":
            ax.scatter(x_data, y_data, color='b')
        elif plot_type == "Bar Chart":
            ax.bar(x_data, y_data, color='c')
        elif plot_type == "Histogram":
            ax.hist(y_data, bins=10, color='m', alpha=0.7)
        elif plot_type == "Pie Chart":
            fig, ax = plt.subplots()
            ax.pie(y_data, labels=x_data, autopct='%1.1f%%', startangle=140)
        elif plot_type == "Box Plot":
            sns.boxplot(data=y_data, ax=ax)
        elif plot_type == "Area Plot":
            ax.fill_between(range(len(x_data)), y_data, color='skyblue', alpha=0.5)
        elif plot_type == "Stem Plot":
            ax.stem(x_data, y_data, linefmt='b-', markerfmt='bo', basefmt='r-')
        elif plot_type == "Heatmap":
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        elif plot_type == "Stack Plot":
            ax.stackplot(range(len(x_data)), y_data, labels=x_data, colors=['b', 'g', 'r', 'c', 'm'])
        elif plot_type == "Error Bar Plot":
            ax.errorbar(x_data, y_data, yerr=5, fmt='o', ecolor='r', capsize=5)
        elif plot_type == "Step Plot":
            ax.step(x_data, y_data, where='mid', color='b')
        elif plot_type == "Hexbin Plot":
            ax.hexbin(range(len(y_data)), y_data, gridsize=20, cmap='Blues')
        elif plot_type == "Contour Plot":
            ax.tricontourf(range(len(y_data)), y_data, y_data, cmap='coolwarm')
        elif plot_type == "Quiver Plot":
            ax.quiver(range(len(y_data)), y_data, range(len(y_data)), y_data)
        else:
            st.error(f"Visualization type '{plot_type}' is not supported.")
        
        # Add labels and title
        ax.set_xlabel(data_dict_obj["xAxis_label"])
        ax.set_ylabel(data_dict_obj["yAxis_label"])
        ax.set_title(f'{plot_type} Visualization')
        ax.grid(True)
        
        # Show the plot in Streamlit
        # st.pyplot(fig)
        # st.markdown("--function_end--")
        return fig
    return "please try again"


    






def app():
    import streamlit as st
    
    from openai import OpenAI
    from langchain_utils import invoke_chain
    st.title("Anaplan Chatbot")
    

    from langchain_community.utilities.sql_database import SQLDatabase
    # Create connection
    db_user = st.secrets["db_user"]
    db_password = st.secrets["db_password"]
    port = st.secrets["port"]
    db_host = st.secrets["db_host"]
    db_name = st.secrets["db_name"]
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{port}/{db_name}")

    # Get schema of the database
    schema = db.get_table_info()
    
    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"
    
    # Initialize chat history
    if "messages" not in st.session_state:
        # print("Creating session state")
        st.session_state.messages = []
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            
            from matplotlib import figure as figuretype
            if type(message["content"]) == figuretype.Figure :
                st.pyplot(message["content"])
                st.markdown("----")
            else:
                st.markdown(message["content"])

    
    # Accept user input
    if prompt := st.chat_input("What's in your mind?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
    
        # Display assistant response in chat message container
        with st.spinner("Generating response..."):
            with st.chat_message("assistant"):
                response = get_response(prompt,st.session_state.messages,db,schema)
                if response == "Too Frequent Submissions, Please try again in 60 seconds.":
                    st.markdown("Too Frequent Submissions, Please try again in 60 seconds.")
                else:    
                    # st.write("----------------")
                    st.pyplot(response)
        # st.write(response)        
        st.session_state.messages.append({"role": "assistant", "content": response})
