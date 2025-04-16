# Intelligent Conversational App with Autogen and Bedrock

## Project Description

This project demonstrates the creation of an intelligent conversational application capable of interacting with multiple data sources, including Confluence, Databricks, and external GraphQL APIs. It leverages the power of:

*   **FastAPI:** For efficient and modern API management.
*   **Autogen:** For creating intelligent agents that can collaborate and perform complex tasks.
*   **Bedrock:** To utilize advanced large language models for text generation, reasoning, and code generation (e.g., SQL, GraphQL).

The application is designed to retrieve information, execute queries, and generate responses based on natural language inputs from the user, orchestrating interactions between different agents to handle diverse requests.

**This is the final version of the app, all requirements have been implemented.**

## Features

*   **Conversational Interface:** Natural language interaction using Autogen agents.
*   **Confluence Integration:** Retrieve data from Confluence using PGVector for similarity search.
*   **Databricks Integration:** Retrieve data from Databricks via SQL.
*   **GraphQL API Integration:** Connect and interact with external GraphQL services.
*   **Bedrock Models:** Leverage Bedrock for text generation, reasoning, and SQL/GraphQL query creation.
*   **Agentic Architecture:** Modular design with agents specializing in different tasks.
*   **FastAPI:** Efficient and modern API management using FastAPI.
*   **Long Term Memory**: The application uses state management to maintain the context of the conversations.
* **Conversation history**: You can now see the conversation history with an endpoint.

## Prerequisites

*   Python 3.9+
*   Poetry for dependency management.
*   Access to Anthropic Bedrock models.
*   PGVector database with Confluence embeddings (optional, if using the Confluence integration).
*   Databricks cluster access (optional, if using the Databricks integration).
*   External GraphQL API access (optional, if using the GraphQL integration).

## Installation

1.  Clone the repository:


1.  **Clone the Repository:**
    