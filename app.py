import streamlit.components.v1 as components
import streamlit as st

if 'b-color' not in st.session_state:
    st.session_state['b-color'] = '#099B77'

# Your HTML and JavaScript code goes here
html_code = f"""
<div id="camelotWheel"></div>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
  // Define the data for the outer and inner wheels
  const outerWheelData = [
    {{ key: 'B', color: '{st.session_state['b-color']}' }},
    {{ key: 'A', color: '#099B77' }},
    // ... Add all outer wheel data
  ];

  const innerWheelData = [
    {{ key: 'F#m', color: '#00A9E0' }},
    {{ key: 'Ebm', color: '#C0A9E0' }},
    // ... Add all inner wheel data
  ];

  // Define the dimensions of the wheel
  const width = 600;
  const height = 600;
  const innerWheelRadius = {{ inner: 100, outer: 200 }};
  const outerWheelRadius = {{ inner: 201, outer: 300 }};

  // Create the wheel container
  const svg = d3.select('#camelotWheel').append('svg')
    .attr('width', width)
    .attr('height', height)
    .append('g')
    .attr('transform', `translate(${{width / 2}}, ${{height / 2}})`);

  // Create the arc generator for the outer and inner wheels
  const outerArc = d3.arc()
    .innerRadius(outerWheelRadius.inner)
    .outerRadius(outerWheelRadius.outer);

  const innerArc = d3.arc()
    .innerRadius(innerWheelRadius.inner)
    .outerRadius(innerWheelRadius.outer);

  // Create the pie generator
  const pie = d3.pie()
    .value(1) // Each segment is equal
    .sort(null);

  // Draw the outer wheel segments
  svg.selectAll('.outer-segment')
    .data(pie(outerWheelData))
    .enter().append('path')
    .attr('d', outerArc)
    .attr('fill', d => d.data.color);

  // Draw the inner wheel segments
  svg.selectAll('.inner-segment')
    .data(pie(innerWheelData))
    .enter().append('path')
    .attr('d', innerArc)
    .attr('fill', d => d.data.color);

  // Add text labels to the outer wheel segments
  svg.selectAll('.outer-label')
    .data(pie(outerWheelData))
    .enter().append('text')
    .attr('transform', d => `translate(${{outerArc.centroid(d)}})`)
    .attr('dy', '0.35em')
    .attr('text-anchor', 'middle')
    .text(d => d.data.key)
    .style('fill', '#fff');

  // Add text labels to the inner wheel segments
  svg.selectAll('.inner-label')
    .data(pie(innerWheelData))
    .enter().append('text')
    .attr('transform', d => `translate(${{innerArc.centroid(d)}})`)
    .attr('dy', '0.35em')
    .attr('text-anchor', 'middle')
    .text(d => d.data.key)
    .style('fill', '#fff');

  // Add central label
  svg.append('text')
    .attr('text-anchor', 'middle')
    .attr('dy', '0.35em')
    .style('fill', '#000')
    .style('font-size', '24px')
    .text('Chaemlot Wheel');
</script>
"""

# Use the components.html function to display the HTML in the Streamlit app
components.html(html_code, height=600)

if st.button("Click me"):
    # change color of { key: 'B', color: '#E09B77' }
    st.session_state['b-color'] = '#E09B77'
    st.rerun()
    None