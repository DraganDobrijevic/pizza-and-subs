window.onload = function(){ 

    confBox = document.getElementById('confirmation');

    document.getElementById("order-btn").onclick = () => {
        
        confBox.style.animationIterationCount = 1;
        confBox.style.animationPlayState = 'running';
    }; 

    document.getElementById("no-btn").onclick = () => {
        confBox.style.animationIterationCount = 2;
        confBox.style.animationPlayState = 'running';
    }; 

};

