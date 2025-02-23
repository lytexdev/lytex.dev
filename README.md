# lytex.dev

## Overview
My personal blog website [lytex.dev](https://lytex.dev).

## Installation

### Prerequisites
- docker-compose

**Clone the repository**
```bash
git clone https://github.com/lytexdev/lytex.git
cd lytex
```

**Build and run**
```bash
docker-compose up -d
```

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