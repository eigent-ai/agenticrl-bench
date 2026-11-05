FROM fedora:40@sha256:3c86d25fef9d2001712bc3d9b091fc40cf04be4767e48f1aa3b785bf58d300ed

WORKDIR /app

RUN dnf install -y rpm-build createrepo_c dnf-plugins-core python3-dnf-plugin-versionlock tmux curl && dnf clean all

RUN curl -LsSf https://astral.sh/uv/0.10.11/install.sh | sh

COPY *.spec /tmp/specs/
COPY local-repo.repo /etc/yum.repos.d/local-repo.repo
COPY setup.sh /tmp/setup.sh

RUN chmod +x /tmp/setup.sh && /tmp/setup.sh
