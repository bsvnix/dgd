FROM postgres:15-alpine

# Set environment variables (you can customize these)
ENV POSTGRES_USER=dgduser
ENV POSTGRES_PASSWORD=dgdpassword
ENV POSTGRES_DB=dgd

# Copy initialization script
COPY init.sql /docker-entrypoint-initdb.d/
