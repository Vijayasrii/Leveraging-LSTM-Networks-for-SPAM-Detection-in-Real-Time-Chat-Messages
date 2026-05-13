graph TD
    A[User Browser] -->|HTTP Request| B[Django Views]
    B -->|Process Request| C[Chat Models]
    C -->|ORM Operations| D[(PostgreSQL Database)]
    B -->|Text Processing| E[TextPreprocessing Module]
    E -->|NLP Analysis| F[Message Classification]
    B -->|Render Template| G[HTML Templates]
    G -->|Static Assets| H[CSS/JS/Images]
    
    subgraph Django Project
        B
        C
        G
    end
    
    subgraph ML Component
        E
        F
    end