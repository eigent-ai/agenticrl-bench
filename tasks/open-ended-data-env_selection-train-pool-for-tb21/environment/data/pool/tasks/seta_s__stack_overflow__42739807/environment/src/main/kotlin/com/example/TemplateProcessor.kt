package com.example

object TemplateProcessor {

    fun loadTemplate(name: String): String {
        val stream = TemplateProcessor::class.java.classLoader
            .getResourceAsStream("/templates/$name")
            ?: throw IllegalStateException("Template not found: $name")
        return stream.bufferedReader().readText()
    }

    fun render(templateName: String, variables: Map<String, String>): String {
        var content = loadTemplate(templateName)
        variables.forEach { (key, value) ->
            content = content.replace("{{$key}}", value)
        }
        return content
    }
}
