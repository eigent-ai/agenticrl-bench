// Application configuration — deeply nested settings
// Do not modify — loaded from environment defaults

const config = {
  database: {
    connection: {
      pool: {
        settings: {
          timeout: {
            value: 30000,
            unit: "ms"
          },
          maxRetries: 5
        },
        minConnections: 2,
        maxConnections: 20
      },
      host: "localhost",
      port: 5432
    },
    name: "app_production"
  },
  server: {
    middleware: {
      cors: {
        options: {
          headers: {
            allowed: ["Content-Type", "Authorization", "X-Request-ID"],
            exposed: ["X-RateLimit-Remaining"]
          },
          credentials: true
        },
        enabled: true
      },
      rateLimit: {
        window: {
          duration: {
            seconds: 60,
            sliding: true
          },
          maxRequests: 100
        }
      }
    },
    port: 8080
  },
  logging: {
    transports: {
      file: {
        rotation: {
          policy: {
            maxSize: "50MB",
            maxFiles: 10,
            compress: true
          }
        },
        path: "/var/log/app"
      },
      console: {
        colorize: true,
        level: "info"
      }
    }
  }
};

module.exports = config;
