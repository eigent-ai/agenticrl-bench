package com.example

import java.util.Properties

object ResourceLoader {

    fun loadConfig(): Properties {
        val props = Properties()
        val stream = ResourceLoader::class.java.getResourceAsStream("config/app.properties")
            ?: throw IllegalStateException("Configuration file not found on classpath: config/app.properties")
        stream.use { props.load(it) }
        return props
    }

    fun loadLines(resourcePath: String): List<String> {
        val stream = ResourceLoader::class.java.classLoader
            .getResourceAsStream(resourcePath)
            ?: throw IllegalStateException("Resource not found: $resourcePath")
        return stream.bufferedReader().readLines()
    }
}
