# Webex-Skill-GPT
## What's this?
It's a simple integration between Cisco's Webex Skill SDK and ChatGPT Library.

## Sounds cool, what does it do?
It basically forwards all of you inquiries to this Webex Assistant Skill to ChatGPT

## You are telling me that I can use ChatGPT from my Webex Devices? IT'S AWESOME!!
Yeah, that's basically what it does and yes I agree it's indeed pretty cool.


# Installation
## So how does it work? Please tell me it's not (too) complicated...
I would say it's pretty simple since I've containerized the whole thing to make it more portable and as much easy to use as possible, so that you don't have to fiddle with SDKs and stuff.
I'm going to explain the logic behind this on day in the following section, but for now just jump to the TL;DR section.

## Here I will explain the whole logic some day... but not today.
Please be patient...

# TL;DR
### Prerequisites
- A Linux server with Docker installed (or any other container tool of your choice, e.g. podman + buildah... I used Docker though).
- A public fully qualified domain name and reachability from the Internet on 443 TCP port.
- Public certificate for your fqdn (you can use Let's Encrypt to generate them or buy them from your preferred provider).

### Installation walkthrough
This is what it looks like to fire it up it on a virtual private server, but you could as well build your container image and deploy it in your preferred cloud container, or just scrap the ngnix layer altogether and use a lambda function... I'll try to enrich with other deploy scenarios in the future.

1. Clone the repo
    ```
    git clone https://github.com/bbird81/webex-skill-gpt.git
    cd webex-skill-gpt
    ```
2. Use your certificate
    - **Rename** your certificate chain and key as `cert-chain.pem` and `priv.key`; they must be in Base64 format.
    - **Copy** your certificate chain+key in `/containers/nginx-reverse-proxy/certificates` directory.

3. Fire up your container  
    Use docker compose to build and start your containers.
    Fill the ENV_file with your OpenAI API token and FQDN of your server and compose:
    ```
    docker compose --env-file ENV_file up -d
    ```
4. Create the skill  
    Create the skill following [this](https://developer.webex.com/docs/api/guides/webex-assistant-skills-guide-developer-portal-guide#creating-a-skill) tutorial.
    Secret and public key can be found in the output of the docker compose logs, by issuing:
    ```
    docker compose logs
    ```
    or just the backend container:
    ```
    docker logs webex-assistant-demo-uvicorn-backend-1
    ```
    _Please pay attention that the URL in the Webex Skill portal **MUST** end with /parse_
5. Proceed to enable the skill in [Webex Control Hub](https://admin.webex.com)
6. Test & Invoke it!  
    You might want to test it using (this)[https://assistant-web.intelligence.webex.com/] web tool or, if you're feeling lucky, just try it on a compatible device using the expression:  
    **"Hey Webex, tell \<your skill name\> \<your request to ChatGPT\>".**  
    The complete guide can be found here:  
    https://developer.webex.com/docs/api/guides/webex-assistant-skills-guide