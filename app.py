import os
import streamlit as st 
# from elastic import elastic
from neo4j_db.generate_cypher import genCypher
from llm import call_model
import matplotlib.pyplot as plt
from openai import OpenAI
from dotenv import load_dotenv
client = OpenAI()
from neo4j_db.neo4j_vector import neo_vector_Documents
from llm import call_openai

load_dotenv(".env")

#Streamlit UI
st.title("💰🕸️💳 Graph HybridRAG Spending Insights")

question = st.text_input("Insert question here")

if question:
    # Generate Cypher query and response
    response, db_response = genCypher(question)

    # Create the Neo4jVector instance and perform similarity search
    vector_index = neo_vector_Documents(question)
    vector_response = vector_index.similarity_search(question, k=1)

    # Format the response for OpenAI
    vendor_index_text = "\n".join([str(res) for res in vector_response])

    # System and user prompts for OpenAI
    system_prompt = "You are a helpful assistant."
    user_prompt = f"{question}\n{vendor_index_text}"

    # Call the OpenAI model and get the response
    vector_ai_response = call_openai(system_prompt, user_prompt)

     # Display responses in Streamlit
    st.markdown(f"**LLM Cypher Agent Response**: {response}")
    #st.markdown(f"**Raw graph data:** {str(db_response)}")
    st.markdown(f"**VectorRAG Response:** {vector_ai_response}")

# if question:
#     elasticsearch_output= elastic(question)
#     neo4j_output = genCypher(question)

# col1, col2 = st.columns(2)

# with col1:
#     if question:
#         st.markdown(f"**Elastic Search** \n {elasticsearch_output}")
    
# with col2:
#     if question:
#         st.markdown(f"**Neo4j** \n {neo4j_output}")

### 

### GENERATE CHART -------------------------------------
# Generate Chart
    if st.button('Generate Chart'):

        def generate_chart(db_response):
            user_prompt = ''
            chart_prompt = "You are an AI that generates Python scripts for Matplotlib charts. Only write python code for the chart, nothing else. Create a chart with darkmode background based on this data: " + str(db_response)
            generate_chart = call_openai(chart_prompt, user_prompt)
            return generate_chart

        def sanitize_script(script):
            # Remove any markdown formatting or text before/after the actual code
            if script.startswith("```python"):
                script = script[9:]  # Remove the initial "```python"
            if script.endswith("```"):
                script = script[:-3]  # Remove the final "```"
            return script.strip()

        def execute_script(script):
            sanitized_script = sanitize_script(script)
            try:
                exec(sanitized_script, globals())
            except Exception as e:
                st.error(f"An error occurred while executing the script: {e}")

        with st.spinner('Generating graph script...'):
            script = generate_chart(db_response)
            
            # Execute and display the script
            st.write("### Chart")
            execute_script(script)
            st.pyplot(plt)

            st.write('### Code')
            st.write(script)

    