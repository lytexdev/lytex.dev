# lytex

## Overview
Personal website built with Flask, featuring blog posts: [lytex.dev](https://lytex.dev)

## Installation

### Prerequisites
- docker-compose

**Clone the repository**
```bash
git clone https://github.com/lytexdev/lytex.git
cd lytex
```

**Build and run the Docker image**
```bash
# with docker-compose-v2
docker compose up -d

# with docker-compose-v1
docker-compose up -d
```
By default it runs on port 8999

## Usage

#### Add a new blog:
```bash
docker exec -it lytex-web-1 sh -c "./blog add 'Title' 'Chapter/ArticleName' 'Markdown Path' ['Author1, Author2']"
```
#### Delete a blog:
```bash
docker exec -it lytex-web-1 sh -c "./blog delete <ID>"
```

## License
This project is licensed under the Creative Commons Legal Code License. See the [LICENSE](LICENSE) file for details.