<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Stargazers][stars-shield]][stars-url]
[![Mainabilities][mainabilities-shield]][mainabilities-url]
[![Build][build-shield]][build-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Style77/dealscan">
    <img src="dealscan/static/images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Dealscan</h3>

  <p align="center">
    Car offers aggregator for car dealers.
    <br />
    <a href="https://github.com/Style77/dealscan"><strong>Explore »</strong></a>
    <br />
    <br />
    <a href="https://dealscan.joachimhodana.com">View</a>
    ·
    <a href="https://github.com/Style77/dealscan/issues">Report Bug</a>
    ·
    <a href="https://github.com/Style77/dealscan/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <ul>
            <li>
                <a href="#development">Development</a>
            </li>
            <li>
                <a href="#production">Production</a>
            </li>
        </ul>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

[![Dealscan Screenshot][product-screenshot]](https://github.com/style77/newsltr)

Dealscan is car offers aggregator, written in Django with use of Alpine.js and HTMX.
It makes you as a car dealer faster. Project is open source, check out the [Roadmap](#roadmap) and [Contributing](#contributing) section to see how you can help.

Checkout the [demo](https://dealscan.joachimhodana.com) or [host it yourself](#getting-started).

If you don't want to host it yourself, you can use the hosted version at [dealscan.joachimhodana.com](https://dealscan.joachimhodana.com).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

* [![Python][Python]][Python-url]
* [![Django Rest Framework][Django]][Django-url]
* [![PostgreSQL][PostgreSQL]][PostgreSQL-url]
* [![Docker][Docker]][Docker-url]
* [![Docker Compose][Docker-Compose]][Docker-Compose-url]
* [![Alpine.js][Alpine.js]][Alpine.js-url]
* [![HTMX][HTMX]][HTMX-url]
* [![Tailwind][Tailwind]][Tailwind-url]
* [![Terraform][Terraform]][Terraform-url]
* [![GitHub Actions][GitHub-Actions]][GitHub-Actions-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Getting Started

This is an example of how to setup dealscan locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an list of things you need to use the software for development purposes and how to install them.
* [Docker](https://docs.docker.com/install/)
* [Docker-compose](https://docs.docker.com/compose/install/)
* [Makefile](https://www.gnu.org/software/make/)
* [Git](https://git-scm.com/downloads)
* [Python 3](https://www.python.org/downloads/)
* [Makefile](https://www.gnu.org/software/make/) (optional)


### Installation

#### Development

1. Install [Docker](https://docs.docker.com/install/) and [Docker-compose](https://docs.docker.com/compose/install/)
2. Clone repository `git clone https://github.com/style77/dealscan.git` and `cd dealscan`
3. Run `cp .env.example .env` and fill in the environment variables
4. Go back to the root directory with `cd ..` and run `make run` to start the development API environment (this will take a while)

#### Production

##### <b>Terraform</b>

Coming soon...

##### <b>VPS</b>

All the following steps are done on the VPS. You should have a user with sudo privileges and a ssh key and ubuntu 20.04/debian installed.

1. Install [Docker](https://docs.docker.com/install/) and [Docker-compose](https://docs.docker.com/compose/install/)
2. Clone repository `git clone https://github.com/style77/dealscan.git` and `cd dealscan`
3. Run `cp .env.example .env` and fill in the environment variables, or set up the environment variables manually with `export`
5. Run `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d`
6*. You can also set up NGINX with the following configuration or just set your domain to the IP of the VPS and the port of the API (8000):

```
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

- More sources
- More filters
- More tests
- More documentation
- subscription management
- password change
- more account settings
- support
- notifications (email, telegram, sms)
- translations

See the [open issues](https://github.com/Style77/newsltr/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. See `CONTIBUTING` for more information.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the CC BY-NC-ND License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

[Joachim Hodana](https://www.linkedin.com/in/joachim-hodana-33815b245/) ([stylek777@gmail.com](mailto:stylek777@gmail.com))

Project Link: [https://github.com/Style77/dealscan](https://github.com/Style77/dealscan)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!-- Shields -->
[contributors-shield]: https://img.shields.io/github/contributors/style77/newsltr?style=for-the-badge
[contributors-url]: https://github.com/Style77/newsltr/graphs/contributors
[stars-shield]: https://img.shields.io/github/stars/style77/newsltr?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[mainabilities-shield]: https://img.shields.io/codeclimate/maintainability/Style77/newsltr?style=for-the-badge
[mainabilities-url]: https://codeclimate.com/github/Style77/newsltr
[technical-debt-shield]: https://img.shields.io/codeclimate/tech-debt/Style77/newsltr?style=for-the-badge&logoColor=red&color=red
[technical-debt-url]: https://codeclimate.com/github/Style77/newsltr
[build-shield]: https://img.shields.io/github/actions/workflow/status/Style77/dealscan/build.yml?label=Build&style=for-the-badge
[build-url]: https://github.com/Style77/dealscan
<!-- Images -->
[product-screenshot]: dealscan/static/images/demo_screenshot.png
<!-- Made with -->
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[Redux]: https://img.shields.io/badge/redux-764ABC?style=for-the-badge&logo=redux&logoColor=white
[Redux-url]: https://redux.js.org/
[Python]: https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Django]: https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[Django-Rest-Framework]: https://img.shields.io/badge/django_rest_framework-092E20?style=for-the-badge&logo=django&logoColor=white
[DRF-url]: https://www.django-rest-framework.org/
[Docker]: https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[Docker-Compose]: https://img.shields.io/badge/docker_compose-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-Compose-url]: https://docs.docker.com/compose/
[Kubernetes]: https://img.shields.io/badge/kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white
[Kubernetes-url]: https://kubernetes.io/
[Helm]: https://img.shields.io/badge/helm-326CE5?style=for-the-badge&logo=helm&logoColor=white
[Helm-url]: https://helm.sh/
[PostgreSQL]: https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[Redis]: https://img.shields.io/badge/redis-DC382D?style=for-the-badge&logo=redis&logoColor=white
[Redis-url]: https://redis.io/
[Celery]: https://img.shields.io/badge/celery-37814A?style=for-the-badge&logo=celery&logoColor=white
[Celery-url]: https://docs.celeryproject.org/en/stable/
[Alpine.js]: https://img.shields.io/badge/alpine.js-8BC0D0?style=for-the-badge&logo=javascript&logoColor=white
[Alpine.js-url]: https://alpinejs.dev/
[Tailwind]: https://img.shields.io/badge/tailwindcss-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white
[Tailwind-url]: https://tailwindcss.com/
[HTMX]: https://img.shields.io/badge/htmx-1A202C?style=for-the-badge&logo=html5&logoColor=white
[HTMX-url]: https://htmx.org/
[Terraform]: https://img.shields.io/badge/terraform-623CE4?style=for-the-badge&logo=terraform&logoColor=white
[Terraform-url]: https://www.terraform.io/
[GitHub-Actions]: https://img.shields.io/badge/github_actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white
[GitHub-Actions-url]: https://github.com/features/actions