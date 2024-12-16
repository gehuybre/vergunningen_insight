document.addEventListener('DOMContentLoaded', function () {
    function revealTimeSeries() {
        const containers = document.querySelectorAll('.chart-and-text-container');

        containers.forEach(container => {
            const chartContainer = container.querySelector('.chart-container');
            const textExplanation = container.querySelector('.text-explanation');
            const iframe = chartContainer.querySelector('iframe');

           if (!iframe) {
             //if no iframe exists. assume this is a plotly graph
             const plotContainer = container.querySelector('.grafiek-container');
             if(plotContainer) {
                const plotDiv = plotContainer.querySelector('.plotly-graph-div');
                if (plotDiv){
                  const windowHeight = window.innerHeight;
                  const containerTop = plotContainer.getBoundingClientRect().top;
                  const revealPoint = 150;

                  if(containerTop < windowHeight - revealPoint){
                    //if the section is in view. reveal the text
                    textExplanation.classList.add('active');

                   //reveal the graph
                    const lines = plotDiv.querySelectorAll('g.traces.scatter > g.points > g.point');
                     lines.forEach((line, index)=>{
                        if(index < (lines.length * ((windowHeight-containerTop)/windowHeight))){
                          line.classList.add('active');
                        }else {
                          line.classList.remove('active')
                        }
                     })
                   }else{
                       textExplanation.classList.remove('active');
                       const lines = plotDiv.querySelectorAll('g.traces.scatter > g.points > g.point');
                       lines.forEach(line => line.classList.remove('active'));
                  }
               }
             }
             return;
           }



            const windowHeight = window.innerHeight;
            const containerTop = chartContainer.getBoundingClientRect().top;
            const revealPoint = 150;

           if (containerTop < windowHeight - revealPoint) {
               textExplanation.classList.add('active'); // Reveal text
                if(iframe && iframe.contentDocument){
                  const chartBody = iframe.contentDocument.body
                  const lines = chartBody.querySelectorAll('g.traces.scatter > g.points > g.point');

                  lines.forEach((line, index)=>{
                    if(index < (lines.length * ((windowHeight-containerTop)/windowHeight))){
                        line.classList.add('active');
                    }else{
                        line.classList.remove('active');
                    }
                  })
                }
           }else{
               textExplanation.classList.remove('active');
               if(iframe && iframe.contentDocument){
                 const chartBody = iframe.contentDocument.body
                 const lines = chartBody.querySelectorAll('g.traces.scatter > g.points > g.point');
                  lines.forEach(line => line.classList.remove('active'));
               }

           }
        });
    }

    window.addEventListener('scroll', revealTimeSeries);
    revealTimeSeries();
});