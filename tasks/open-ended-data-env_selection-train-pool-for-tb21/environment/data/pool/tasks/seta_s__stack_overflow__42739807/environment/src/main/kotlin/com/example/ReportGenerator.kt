package com.example

object ReportGenerator {

    fun generateReport(title: String, body: String): String {
        val config = ResourceLoader.loadConfig()
        val version = config.getProperty("app.version") ?: "unknown"
        return TemplateProcessor.render(
            "report.html",
            mapOf(
                "title" to title,
                "body" to body,
                "version" to version
            )
        )
    }
}
