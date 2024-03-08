
document.addEventListener('DOMContentLoaded', () => {
    
    var socket = io.connect('http://localhost:12345');
    
    socket.on('update_progress_lungo', function(data1) {
        console.log('Message received: ', data1);
        let progress = data1.weight_lungo
        const progressBar = document.getElementById('progress-bar-lungo');
        // const progressSpan = document.getElementById('progress');
        progress = progress * 10
        progress = Math.min(progress, 100);
        
        progressBar.style.width = progress + '%';
        if (progress <= 20) {
            progressBar.classList.add('blinking');
        } else {
            progressBar.classList.remove('blinking');
        }
        }
    );

    socket.on('update_progress_americano', function(data2) {
        console.log('Message received: ', data2);
        let progress = data2.weight_americano
        const progressBar = document.getElementById('progress-bar-americano');
        // const progressSpan = document.getElementById('progress');
        progress = progress * 10
        progress = Math.min(progress, 100);
        
        progressBar.style.width = progress + '%'; 
    });

    socket.on('update_progress_espresso', function(data3) {
        console.log('Message received: ', data3);
        let progress = data3.weight_espresso
        const progressBar = document.getElementById('progress-bar-espresso');
        // const progressSpan = document.getElementById('progress');
        progress = progress * 10
        progress = Math.min(progress, 100);

        progressBar.style.width = progress + '%'; 
    });




    // const interval = setInterval(() => {
    //         progress = progress * 10
    //         progressBar.style.width = progress + '%';        
    // }, 10); // 10ms마다 실행
});
