[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/bbird81/webex-skill-gpt)  

# Webex-Skill-GPT
## What's this?
It's a simple integration between Cisco's Webex Skill SDK and ChatGPT Library.

## Sounds cool, what does it do?
It basically forwards all of your inquiries to this Webex Assistant Skill to ChatGPT.

## You are telling me that I can use ChatGPT from my Webex Devices? IT'S AWESOME!!
Yeah, that's basically what it does and yes I agree it's indeed pretty cool.

## It's too good to be true, must be black magic... How does it work?
For now we'll settle for this (very) high level design to give you an idea of how it's done.

![Schema of the application](wbx-skill-gpt-schema.png)
(Yes, this schema is done with [excalidraw](https://excalidraw.com/))

# Installation
### So how does it work? Please tell me it's not (too) complicated...
I would say it's pretty simple since I've containerized the whole thing to make it more portable and as much easy to use as possible, so that you don't have to fiddle with SDKs and stuff.
I'm going to explain the logic behind this one day in the following section, but for now just jump to the TL;DR section.

### Prerequisites
- A Linux server with Docker installed (or any other container tool of your choice, e.g. podman + buildah... I used Docker though).
    - **TIP**: you can use the docker script to quickly install docker on supported distros on a development environment:
        ```
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        ```
        You can get more details on installing docker [here](https://docs.docker.com/engine/install/).
          
- A public fully qualified domain name pointing to your VPS hosting the containers and reachability from the Internet on 443 TCP port.
- Public certificate for your fqdn.
    - **TIP**: You can use [certbot](https://certbot.eff.org/) to generate a 3 months public certificate from Let's Encrypt.  
    Certbot can be launched in a container:
        ```
        sudo docker run -it --rm --name certbot \
                -v "/etc/letsencrypt:/etc/letsencrypt" \
                -v "/var/lib/letsencrypt:/var/lib/letsencrypt" \
                -p 80:80 \
                certbot/certbot certonly
        ```
        This will start a wizard, which will ask for your fqdn, an email and a couple more personal information.
        If you give reachability from the Internet on port 80, you can do everything locally (option 1 of certbot wizard).
        Once finished, your certificate+key will be saved in  
        `/etc/letsencrypt/live/ ->your fqdn<- /fullchain.pem`  
        `/etc/letsencrypt/live/ ->your fqdn<- /privkey.pem`  
- OpenAI account with an API token

### Installation walkthrough
This is what it looks like to fire it up it on a virtual private server, but you could as well build your container image and deploy it in your preferred cloud container, or just scrap the ngnix layer altogether and use a lambda function... I'll try to enrich with other deploy scenarios in the future.

1. Clone the repo
    ```
    git clone https://github.com/bbird81/webex-skill-gpt.git
    cd webex-skill-gpt
    ```
2. Use your certificate
    - **Rename** your certificate chain and key as `fullchain.pem` and `privkey.pem`; they must be in Base64 format (_if you used certbot, files already have these names_).
    - **Copy** your certificate chain+key in `containers/nginx-reverse-proxy/certificates` directory.

3. Fire up your container  
    Use docker compose to build and start your containers.  

    3.1. Edit .env file with your favourite editor and fill OpenAI API token and FQDN of your server:
    ```
    # Insert OpenAPI token below
    OPENAPI_KEY = "..."
    # Fully Qualified Domain Name of your Webex Skill URL
    FQDN = "..."
    ```
    3.2. Do docker compose:
    ```
    docker compose up -d
    ```
4. Create the skill  
    Create the skill following [this](https://developer.webex.com/docs/api/guides/webex-assistant-skills-guide-developer-portal-guide#creating-a-skill) tutorial.  
    \** _Please pay attention that the URL in the Webex Skill portal **MUST** end with /parse_ \**  
    Secret and public key can be found in the output of the docker compose logs, by issuing:
    ```
    docker compose logs
    ```
    For further details on logs, please check the Troubleshooting section

5. Proceed to enable the skill in [Webex Control Hub](https://admin.webex.com)
6. Test & Invoke it!  
    You might want to test it using [this](https://assistant-web.intelligence.webex.com/) web tool or, if you're feeling lucky, just try it on a compatible device using the expression:  
    **"Hey Webex, tell \<your skill name\> \<your request to ChatGPT\>".**  
    The complete guide for creating a generic Webex Assistant Skill can be found here:  
    https://developer.webex.com/docs/api/guides/webex-assistant-skills-guide

## Troubleshooting
Everybody knows this: you can't win them all :-/  
You might have received some errors during the installation, I'm going to address the most common here; please open a issue if all of this doesn't work for you and I'll see what I can do.  

**Never forget that this is a proof of concept and provided "as is"** so mind that every effort from my side is **BEST EFFORT**: please be kind and patient.

### Common `docker compose logs' strange outputs:  
* If you don't set OpenAI token or FQDN of your vps in the .env file, you will get the following messages:
    ```
    webex-skill-gpt-uvicorn-backend-1  | OpenAI API token not set: ABORTING!
    webex-skill-gpt-nginx-reverse-proxy-1  | FQDN env var not set: ABORTING!
    ```
    Set the values in the `.env` file and **rebuild** the container images with the following command:  
    `docker compose up -d --build --force-recreate`  
    To see only the latest run of docker compose logs, you might use the --since parameter, in the example you'll see log of the last 3 minutes:  
    `docker compose logs --since 3m`
* Certificate/Private key not in base64 format.  
    If the certificate/key you put in `containers/nginx-reverse-proxy/certificates` directory are not in base64 format, an error like this might show:
    ```
    webex-skill-gpt-nginx-reverse-proxy-1  | 2023/06/28 16:30:28 [emerg] 10#10: cannot load certificate "/etc/ssl/certs/nginx/fullchain.pem": PEM_read_bio_X509_AUX() failed (SSL: error:04800064:PEM routines::bad base64 decode)
    webex-skill-gpt-nginx-reverse-proxy-1  | nginx: [emerg] cannot load certificate "/etc/ssl/certs/nginx/fullchain.pem": PEM_read_bio_X509_AUX() failed (SSL: error:04800064:PEM routines::bad base64 decode)
    ```
    If the extention of your certificate/private key is .cer, .der or .pfx, then it might be in binary format.
    You can check by using cat/less/more followed by the file name, certificate and key should look something like this:
    ```
    -----BEGIN CERTIFICATE-----
    IUUouds90udsab91290ueubei39329 ... some multi-line rubbish here ...
    -----END CERTIFICATE-----

    -----BEGIN PRIVATE KEY-----
    UUouds90udsab91290ueubei39329 ... some multi-line rubbish here ...
    -----END PRIVATE KEY-----
    ```
    To convert a certificate from binary to base64 format you might use [`openssl`](https://knowledge.digicert.com/solution/SO26449.html). Also Google (or Duck Duck GO!) is your friend :-).


 