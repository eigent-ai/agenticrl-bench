package com.example

fun main(args: Array<String>) {
    val title = args.getOrElse(0) { "Default Report" }
    val body  = args.getOrElse(1) { "No content provided." }
    println(ReportGenerator.generateReport(title, body))
}
