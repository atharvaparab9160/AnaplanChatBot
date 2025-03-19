def app():
    import streamlit as st
    
    from openai import OpenAI
    from langchain_utils import invoke_chain
    st.title("Anaplan Chatbot")
    
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
                # st.markdown("----")
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
                response = invoke_chain(prompt,st.session_state.messages)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

