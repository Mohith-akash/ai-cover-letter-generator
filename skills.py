
# Tool alternatives - if job asks for X and you have Y, mention Y as transferable
TOOL_ALTERNATIVES = {
    # BI/Visualization/Frontend
    "tableau": ["power bi", "streamlit"],
    "looker": ["power bi", "streamlit"],
    "metabase": ["power bi", "streamlit"],
    "superset": ["power bi", "streamlit"],
    "quicksight": ["power bi", "streamlit"],
    "domo": ["power bi", "streamlit"],
    "qlik": ["power bi", "streamlit"],
    "spotfire": ["power bi", "streamlit"],
    "microstrategy": ["power bi", "streamlit"],
    "react": ["streamlit"],  # For data apps
    "vue": ["streamlit"],
    
    # Orchestration & Workflow
    "airflow": ["dagster"],
    "prefect": ["dagster"],
    "luigi": ["dagster"],
    "mage": ["dagster"],
    "kestra": ["dagster"],
    "temporal": ["dagster"],
    "control-m": ["dagster"],  # Legacy
    "autosys": ["dagster"],    # Legacy
    "azure data factory": ["dagster", "dbt", "azure"], # Code-first replacement
    
    # Data Transformation & Modeling
    "dataform": ["dbt", "dbt core"],
    "sqlmesh": ["dbt", "dbt core"],
    "coalesce": ["dbt"],
    "matillion": ["dbt", "python"],
    "informatica": ["dbt", "python", "databricks"], # Legacy to Modern
    "talend": ["dbt", "python", "databricks"],
    "ssis": ["dbt", "python", "azure"],
    "pentaho": ["dbt", "python"],
    
    # Ingestion / ETL / ELT
    "fivetran": ["python", "dlt", "azure event hub"], # Custom pipelines
    "airbyte": ["python", "dlt", "azure event hub"],
    "stitch": ["python", "dlt"],
    "meltano": ["python", "dlt"],
    "kafka connect": ["azure event hub", "python"],
    
    # Cloud Platforms & Infrastructure
    "aws": ["azure"],
    "gcp": ["azure"],
    "snowflake": ["databricks"],
    "redshift": ["databricks", "duckdb"],
    "bigquery": ["databricks", "duckdb"],
    "synapse": ["databricks", "azure"],
    "teradata": ["databricks"], # Legacy
    "oracle": ["databricks", "sql"],
    "sql server": ["azure", "sql"],
    "fabric": ["databricks", "power bi"],
    
    # Streaming & Real-time
    "kafka": ["azure event hub", "spark", "delta live tables"],
    "kinesis": ["azure event hub"],
    "pulsar": ["azure event hub"],
    "redpanda": ["azure event hub"],
    "warpstream": ["azure event hub"],
    "flink": ["spark", "structured streaming"],
    
    # Table Formats & Storage
    "iceberg": ["delta lake"],
    "hudi": ["delta lake"],
    "minio": ["azure", "delta lake"],
    "s3": ["azure blob storage"],
    
    # Processing & Compute
    "spark": ["polars", "databricks", "pyspark"],
    "pandas": ["polars"],
    "dask": ["polars", "spark"],
    "ray": ["spark"],
    "hadoop": ["spark", "databricks"], # Legacy
    "hive": ["spark", "sql"],
    
    # Data Quality & Observability
    "soda": ["great expectations", "dlt expectations"],
    "monte carlo": ["great expectations", "dlt expectations"],
    "anomalo": ["great expectations"],
    "great expectations": ["dlt expectations"],
    
    # Governance & Catalog
    "atlan": ["unity catalog"],
    "alation": ["unity catalog"],
    "collibra": ["unity catalog"],
    "amundsen": ["unity catalog"],
    "datahub": ["unity catalog"],
    "polaris": ["unity catalog"],
    
    # Languages
    "scala": ["python", "pyspark"],
    "java": ["python"],
    "r": ["python", "polars"],
    "julia": ["python"],
    
    # Databases (OLAP/OLTP)
    "clickhouse": ["duckdb", "databricks"],
    "starrocks": ["duckdb", "databricks"],
    "druid": ["duckdb", "databricks"],
    "postgresql": ["sql"],
    "mysql": ["sql"],
    "dynamodb": ["azure"],
    "cosmos db": ["azure"],
    "trino": ["databricks", "duckdb"],
    "presto": ["databricks", "duckdb"],
    "athena": ["databricks", "duckdb"],
    
    # AI/ML
    "openai": ["cerebras", "gemini", "llm"],
    "anthropic": ["cerebras", "gemini", "llm"],
    "langsmith": ["langchain"],
    "mlflow": ["databricks"],
    "kubeflow": ["dagster", "databricks"],
    "sagemaker": ["databricks", "python"],
    "vertex ai": ["databricks", "python"],
    
    # AWS-specific (common in job postings)
    "glue": ["dagster", "databricks", "dbt"],
    "emr": ["databricks", "spark"],
    "lambda": ["azure", "python"],
    "step functions": ["dagster"],
    "cloudformation": ["github actions"],
    
    # GCP-specific
    "dataflow": ["spark", "databricks"],
    "dataproc": ["databricks", "spark"],
    "cloud composer": ["dagster"],
    "pub/sub": ["azure event hub"],
    
    # dbt variants
    "dbt cloud": ["dbt core", "dbt"],
    
    # Data Catalogs
    "nessie": ["unity catalog"],
    "openmetadata": ["unity catalog"],
    "marquez": ["unity catalog"],
    
    # Monitoring/Observability
    "grafana": ["streamlit", "power bi"],
    "datadog": ["great expectations"],
    "newrelic": ["great expectations"],
    
    # Notebooks
    "jupyter": ["databricks", "streamlit"],
    "zeppelin": ["databricks"],
    "hex": ["databricks", "streamlit"],
    "deepnote": ["databricks", "streamlit"],
}

# Your skills database with proof/metrics - UPDATED with latest CV data
SKILLS_DATABASE = {
    # Data Engineering - Lakehouse
    "databricks": {
        "proof": "Built 3 production platforms on Databricks (Vortex, Olist, GDELT)",
        "projects": ["Vortex", "Olist"],
        "level": "advanced"
    },
    "delta lake": {
        "proof": "Implemented Medallion architecture (Bronze/Silver/Gold) with Unity Catalog governance",
        "projects": ["Vortex", "Olist"],
        "level": "advanced"
    },
    "delta live tables": {
        "proof": "Real-time streaming with DLT Expectations and <500ms latency",
        "projects": ["Vortex"],
        "level": "advanced"
    },
    "dbt": {
        "proof": "dbt Core transformation layers for 16M+ rows with staging + marts",
        "projects": ["Vortex", "GDELT"],
        "level": "advanced"
    },
    "dbt core": {
        "proof": "Built ELT transformations for cart abandonment analytics and recovery queues",
        "projects": ["Vortex", "GDELT"],
        "level": "advanced"
    },
    "dagster": {
        "proof": "Serverless ELT orchestration via GitHub Actions for zero-cost deployments",
        "projects": ["GDELT", "Vortex"],
        "level": "advanced"
    },
    "azure": {
        "proof": "Azure Event Hub real-time ingestion with 1000+ events/day",
        "projects": ["Vortex"],
        "level": "advanced"
    },
    "azure event hub": {
        "proof": "Real-time streaming ingestion into Delta Live Tables with <500ms latency",
        "projects": ["Vortex"],
        "level": "advanced"
    },
    "streaming": {
        "proof": "Real-time pipeline ingesting 1000+ events/day from Azure Event Hub",
        "projects": ["Vortex"],
        "level": "advanced"
    },
    "polars": {
        "proof": "90% latency reduction (10x faster) processing 16M+ rows",
        "projects": ["GDELT"],
        "level": "advanced"
    },
    "great expectations": {
        "proof": "Data quality validation to improve dataset reliability",
        "projects": ["GDELT"],
        "level": "intermediate"
    },
    
    # Analytics & SQL
    "sql": {
        "proof": "Star schema design, fact/dimension tables, Kimball methodology",
        "projects": ["All"],
        "level": "advanced"
    },
    "python": {
        "proof": "Data engineering, ELT pipelines, API development, automation",
        "projects": ["All"],
        "level": "advanced"
    },
    "power bi": {
        "proof": "Executive dashboards for e-commerce analytics",
        "projects": ["Olist"],
        "level": "advanced"
    },
    "streamlit": {
        "proof": "3 live production apps deployed on Streamlit Cloud",
        "projects": ["Vortex", "GDELT", "Olist"],
        "level": "advanced"
    },
    
    # Data Quality & Governance
    "data quality": {
        "proof": "DLT Expectations for schema/row-level validation with bad-record handling",
        "projects": ["Vortex", "GDELT"],
        "level": "advanced"
    },
    "unity catalog": {
        "proof": "Governance for metadata, lineage, and access control",
        "projects": ["Olist"],
        "level": "intermediate"
    },
    
    # Data Modeling
    "medallion architecture": {
        "proof": "Bronze/Silver/Gold layers on Databricks + Delta Lake",
        "projects": ["Vortex", "Olist"],
        "level": "advanced"
    },
    "dimensional modeling": {
        "proof": "Kimball-style star schema with fact/dimension tables",
        "projects": ["Olist", "GDELT"],
        "level": "advanced"
    },
    "star schema": {
        "proof": "Analytics-ready fact/dimension models for e-commerce data",
        "projects": ["Olist"],
        "level": "advanced"
    },
    "elt": {
        "proof": "Serverless ELT patterns processing 100K+ daily events",
        "projects": ["GDELT", "Vortex"],
        "level": "advanced"
    },
    "etl": {
        "proof": "Built batch and streaming ETL pipelines on Databricks",
        "projects": ["Vortex", "Olist"],
        "level": "advanced"
    },
    
    # DevOps & CI/CD
    "github actions": {
        "proof": "CI/CD for automated data pipeline deployments with zero-cost scheduling",
        "projects": ["GDELT", "Vortex"],
        "level": "advanced"
    },
    "ci/cd": {
        "proof": "Automated pipeline runs with Dagster + GitHub Actions",
        "projects": ["GDELT", "Vortex"],
        "level": "intermediate"
    },
    
    # Cloud & Infrastructure
    "duckdb": {
        "proof": "MotherDuck/DuckDB for serverless analytics",
        "projects": ["GDELT"],
        "level": "intermediate"
    },
    "motherduck": {
        "proof": "Cloud DuckDB for analytics warehouse",
        "projects": ["GDELT"],
        "level": "intermediate"
    },
    
    # AI/ML (from GKG project - not in CV but in earlier data)
    "rag": {
        "proof": "Hybrid RAG system with semantic + keyword search",
        "projects": ["GKG"],
        "level": "intermediate"
    },
    "llm": {
        "proof": "LLM function calling with Gemini API",
        "projects": ["GKG"],
        "level": "intermediate"
    },
    "langchain": {
        "proof": "RAG pipelines and prompt engineering",
        "projects": ["GKG"],
        "level": "intermediate"
    },
    "vector database": {
        "proof": "ChromaDB for 160K+ articles",
        "projects": ["GKG"],
        "level": "intermediate"
    },
}

# Your projects - UPDATED with accurate data from CV
PROJECTS_DATABASE = {
    "vortex": {
        "name": "Vortex: Real-Time Streaming Platform",
        "description": "Real-time streaming pipeline with Azure Event Hub → Delta Live Tables with <500ms latency",
        "metrics": "1000+ events/day, <500ms latency, DLT Expectations for data quality",
        "tech": ["Databricks", "Delta Lake", "Azure Event Hub", "Delta Live Tables", "dbt Core", "Python", "Streamlit"],
        "highlights": [
            "Real-time streaming with <500ms latency",
            "DLT Expectations for schema & row-level validation",
            "Cart abandonment analytics with recovery queue for high-value carts (>$500)",
            "Zero-cost serverless scheduling via GitHub Actions"
        ],
        "link": "https://vortex-the-revenue-recovery-engine.streamlit.app/"
    },
    "gdelt": {
        "name": "Global News Intelligence Platform",
        "description": "Serverless ELT processing 100K+ daily events into 16M+ row warehouse",
        "metrics": "16M+ rows, 100K+ daily events, 90% latency reduction (10x faster)",
        "tech": ["Python", "Polars", "Dagster", "dbt Core", "MotherDuck", "Great Expectations", "GitHub Actions", "Streamlit"],
        "highlights": [
            "Processed 100K+ daily events into 16M+ row warehouse",
            "90% latency reduction using Polars optimization",
            "Great Expectations-style validation checks",
            "Zero-cost deployments via Dagster + GitHub Actions"
        ],
        "link": "https://global-news-intel-platform.streamlit.app/"
    },
    "olist": {
        "name": "Olist E-Commerce Analytics",
        "description": "Databricks Lakehouse with Medallion Architecture (Bronze/Silver/Gold)",
        "metrics": "100K+ orders, Kimball star schema, Unity Catalog governance",
        "tech": ["Databricks", "Delta Lake", "Unity Catalog", "SQL", "Python", "Streamlit", "Power BI"],
        "highlights": [
            "Medallion architecture on Databricks + Delta Lake",
            "Kimball-style star schema with fact/dimension tables",
            "Unity Catalog for governance and lineage"
        ],
        "link": "https://olist-analytics-platform.streamlit.app/"
    },
    "gkg": {
        "name": "GKG Emotion Analytics",
        "description": "Hybrid RAG with Gemini function calling",
        "metrics": "160K+ articles, 2200+ emotion dimensions",
        "tech": ["LangChain", "ChromaDB", "Gemini", "Streamlit"],
        "highlights": [
            "Hybrid RAG with semantic + keyword search",
            "Gemini function calling for text-to-SQL"
        ],
        "link": None
    },
}


def match_skills_keyword(job_text: str) -> list:
    job_lower = job_text.lower()
    matches = []
    
    for skill, data in SKILLS_DATABASE.items():
        if skill in job_lower:
            matches.append({
                "skill": skill,
                "proof": data["proof"],
                "level": data["level"]
            })
    
    return matches


def match_transferable_skills(job_text: str) -> list:
    """
    Find tools the job asks for that you don't have, but you have equivalents.
    Returns: [{"job_needs": "tableau", "you_have": "power bi", "proof": "..."}]
    """
    job_lower = job_text.lower()
    transferable = []
    
    for job_tool, my_alternatives in TOOL_ALTERNATIVES.items():
        # Job asks for this tool
        if job_tool in job_lower:
            # Check if we have any of the alternatives
            for alt in my_alternatives:
                if alt in SKILLS_DATABASE:
                    transferable.append({
                        "job_needs": job_tool,
                        "you_have": alt,
                        "proof": SKILLS_DATABASE[alt]["proof"]
                    })
                    break  # Only need one alternative per tool
    
    return transferable


def get_best_projects(matched_skills: list, top_k: int = 3) -> list:
    core_projects = ["gdelt", "vortex", "olist"]
    
    result = []
    for project_id in core_projects:
        if project_id in PROJECTS_DATABASE:
            result.append(PROJECTS_DATABASE[project_id])
    
    return result

