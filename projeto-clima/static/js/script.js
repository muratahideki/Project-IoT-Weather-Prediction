console.log("JS carregado com sucesso");

function atualizarPagina() {
    location.reload();
}


let ctx = document.getElementById('grafico').getContext('2d');
let chart = new Chart(ctx, {
    type: 'line',
    data: { labels: [], datasets: [ 
        { label: 'Temp', data: [], borderColor: 'red', yAxisID: 'y' }, 
        { label: 'Umid', data: [], borderColor: 'blue', yAxisID: 'y' },
        { label: 'Vento', data: [], borderColor: 'orange', yAxisID: 'y' } 
    ]},
    options: { animation: false }
});

function atualizarGrafico() {
    fetch("/api/brutos").then(res => res.json()).then(dados => {
        let labels = [], temp = [], umid = [], vento = [];
        dados.reverse().forEach(d => {
            labels.push(d[6].split('T')[1].split('.')[0]); // Data é indice 6 agora
            temp.push(d[1]); 
            umid.push(d[4]); 
            vento.push(d[5]); // Vento é indice 5
        });
        chart.data.labels = labels; 
        chart.data.datasets[0].data = temp; 
        chart.data.datasets[1].data = umid; 
        chart.data.datasets[2].data = vento;
        chart.update();
    });
}

setInterval(atualizarGrafico, 3000);
atualizarGrafico();