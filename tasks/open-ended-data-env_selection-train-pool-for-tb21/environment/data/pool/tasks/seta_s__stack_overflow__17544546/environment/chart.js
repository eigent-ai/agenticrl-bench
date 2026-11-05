const { JSDOM } = require('jsdom');
const d3 = require('d3');

function createChart(config) {
    const { width, height, margin } = config;
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
    const document = dom.window.document;

    const body = d3.select(document.body);
    const svg = body.append('svg')
        .attr('xmlns', 'http://www.w3.org/2000/svg')
        .attr('width', width)
        .attr('height', height);

    const chartGroup = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    const scale = d3.scaleLinear()
        .domain([0, 365])
        .range([0, innerWidth]);

    chartGroup.append('rect')
        .attr('width', innerWidth)
        .attr('height', innerHeight)
        .attr('fill', '#f0f4f8')
        .attr('stroke', '#ccc');

    return { svg: chartGroup, scale, dom, innerWidth, innerHeight };
}

module.exports = { createChart };
