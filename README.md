# lytex

## Overview
Personal website built with Flask, featuring blog posts: [lytex.dev](https://lytex.dev).

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

# with docker-compose
docker-compose up -d
```
By default it runs on port 8999

## Usage

#### Add a new blog:
```bash
./blog add 'Title' 'Chapter/ArticleName' 'Markdown/File/Path' ['Author1, Author2']
```
#### Delete a blog:
```bash
./blog delete <ID>
```

## License
This project is licensed under the Creative Commons Legal Code License. See the [LICENSE](LICENSE) file for details.