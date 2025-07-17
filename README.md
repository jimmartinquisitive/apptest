# apptest

## Description

This repository provides a complete solution for deploying a Python Flask web application on Azure, fronted by a secure and highly available Azure Application Gateway v2. The project includes a simple backend application and the necessary Infrastructure as Code (IaC) templates written in Bicep to provision the required Azure networking and security resources.

The primary purpose is to demonstrate a robust architecture where web traffic is managed, secured, and load-balanced by an Application Gateway with an integrated Web Application Firewall (WAF) before reaching the backend application hosted on an Azure App Service.

## Features

-   **Simple Flask Backend**: A lightweight Python web application that returns the hostname of the serving instance, useful for testing load balancing.
-   **Infrastructure as Code (IaC)**: Utilizes a Bicep template (`appgw`) for automated, repeatable, and version-controlled deployment of Azure resources.
-   **Azure Application Gateway v2**: Deploys a highly configurable Application Gateway with support for:
    -   Public and private frontend IP configurations.
    -   Autoscaling for performance and cost-efficiency.
    -   SSL termination using certificates from Azure Key Vault.
-   **Web Application Firewall (WAF)**: Includes a WAF policy with the OWASP 3.2 and Microsoft Bot Manager rule sets to protect the application from common web vulnerabilities and malicious bots.
-   **Highly Parameterized Deployment**: The Bicep template is designed for flexibility, allowing extensive customization of names, SKUs, network settings, and WAF rules.
-   **Azure App Service Integration**: Comes with a `web.config` file for seamless hosting of the Flask application on an Azure App Service (Windows plan).

## Getting Started

Follow these instructions to get a copy of the project up and running in your own Azure environment.

### Prerequisites

-   **Python 3.8+**
-   **An active Azure Subscription**
-   **Azure CLI** or **Azure PowerShell**
-   **Git**

You will need to create a `requirements.txt` file for the Python application:

```text
# requirements.txt
Flask
```

### Installation & Deployment

The deployment process involves two main steps: deploying the Azure infrastructure using Bicep and then deploying the Flask application to the created Azure App Service.

#### 1. Deploy Azure Infrastructure

The Bicep template `appgw` will provision the Application Gateway, WAF Policy, and related networking components.

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/<your-username>/apptest.git
    cd apptest
    ```

2.  **Log in to Azure:**
    ```sh
    az login
    ```

3.  **Create a resource group:**
    ```sh
    az group create --name MyResourceGroup --location "East US"
    ```

4.  **Deploy the Bicep template:**
    The Bicep file is heavily parameterized. It is highly recommended to create a parameter file (`params.json`) to manage your configuration. The `backendFqdn` parameter should be the default hostname of the Azure App Service you intend to create (e.g., `my-cool-app.azurewebsites.net`).

    You can deploy the Bicep file using the Azure CLI. You will need to provide values for parameters such as virtual network names, subnet names, your public IP address resource ID, and the Key Vault secret URI for the SSL certificate.

    ```sh
    # Example deployment command (update parameters accordingly)
    az deployment group create \
      --resource-group MyResourceGroup \
      --template-file appgw \
      --parameters applicationGatewayName=myAppGateway \
                   location="East US" \
                   # ... and all other required parameters
    ```

#### 2. Deploy the Flask Application

After the infrastructure is provisioned, deploy the Python code to the Azure App Service that was configured as the backend pool for the Application Gateway.

1.  **Set up a local Python virtual environment:**
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    pip install -r requirements.txt
    ```

2.  **Deploy to Azure App Service:**
    You can use various methods to deploy the application, such as the `az webapp up` command, VS Code extensions, or setting up a CI/CD pipeline. Make sure to include `app.py`, `web.config`, and `requirements.txt` in your deployment package.

    Example using `az webapp up` (this command can also create the App Service Plan and App Service if they don't exist):
    ```sh
    # Ensure your App Service name matches the `backendFqdn` used in the Bicep deployment
    az webapp up --name <your-app-service-name> --resource-group MyResourceGroup --sku B1
    ```

## Usage

Once both the infrastructure and the application are deployed, you can access the application through the public IP address or DNS name associated with the Azure Application Gateway's public frontend.

Navigate to `https://<your-app-gateway-dns-name>` in your browser.

The expected response from the application will be:

```
Hello, Azure App Gateway! Served from: <hostname-of-the-app-service-instance>
```

The `<hostname>` will be the unique identifier of the specific App Service instance that handled the request. If you have multiple instances scaled out, refreshing the page may show different hostnames, demonstrating the load balancing functionality of the Application Gateway.

## File Structure

```
.
├── app.py              # The main Python Flask application file.
├── appgw               # Bicep template for deploying the Azure Application Gateway and WAF Policy.
└── web.config          # Configuration file for hosting the Python app on IIS / Azure App Service (Windows).
```