
# Bedrock Multi-Agent Conversational Application

## Project Description

This project showcases the development of an intelligent conversational application that interacts with multiple data sources, including Confluence, Databricks, and external GraphQL APIs. The application leverages advanced technologies to provide a seamless conversational experience:

*   **FastAPI**: For building a high-performance RESTful API.
*   **Autogen**: For orchestrating intelligent, collaborative agents.
*   **AWS Bedrock**: For advanced text generation, reasoning, and code generation using large language models.
*   **Pgvector**: For managing embeddings and similarity searches.
* **Uvicorn**: for runing the application.
* **Poetry**: for dependencies management.

The application is designed to retrieve information, execute queries, and generate responses based on natural language inputs. It coordinates interactions between specialized agents to fulfill diverse user requests.

## Features

*   **Natural Language Interface**: Interact with the application using natural language, powered by Autogen.
*   **Confluence Integration**: Query and retrieve information from Confluence using Pgvector for efficient similarity searches.
*   **Databricks Integration**: Execute SQL queries on Databricks to extract and process data.
*   **GraphQL API Integration**: Connect and interact with external GraphQL services to fetch data.
*   **AWS Bedrock LLMs**: Utilize AWS Bedrock's large language models for advanced text generation, reasoning, and code generation (SQL/GraphQL).
*   **Agent Collaboration**: A modular architecture where agents collaborate to perform complex tasks.
*   **FastAPI API**: A high-performance, modern API built with FastAPI.
* **State Management**: Maintain conversation context across multiple interactions.
* **Conversation History**: Retrieve and view conversation history.

## Prerequisites

Before you begin, ensure you have the following:

*   **Python 3.9+**: Ensure you have Python 3.9 or higher installed.
*   **Poetry**: Install Poetry for managing project dependencies:
    

## Installation

1.  Clone the repository:


1.  **Clone the Repository:**
    