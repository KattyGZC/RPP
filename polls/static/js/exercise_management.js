var grabar = document.getElementById('grabar')
var detener = document.getElementById('detener')

var rec;
var text_exercise = '';

const regex = /&quot;/gi
json_exe = json_exe.replace(regex, '"')
json_exe = JSON.parse(json_exe)
console.log(json_exe)
var exe = document.getElementById('exe');
json_exe = json_exe.sort(() => { return Math.random() - 0.5 })
show_exercise()

window.onload = function () {
    detener.style.display = "none";
}

function show_exercise() {
    if (json_exe.length > 0) {
        exercise = json_exe.pop()
        console.log(exercise)
        exe.innerHTML = exercise.fields.text;
    } else {
        //alert('Se terminaron los ejercicios')
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Se terminaron los ejercicios',
        })
    }
}

function on_start(event) {
    for (i = event.resultIndex; i < event.results.length; i++) {
        text_exercise = event.results[i][0].transcript;
    }
    if (text_exercise === '') {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'No has grabado nada',
        })
    } else {
        processed_text(text_exercise)
    }

}

function record_exercise() {
    detener.style.display = "flex";
    grabar.style.display = "none";
    if (!("webkitSpeechRecognition" in window)) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Tu navegador no tiene acceso al reconocimiento de voz',
        })
    } else {
        rec = new webkitSpeechRecognition();
        rec.lang = "es-EC"
        rec.continuous = true
        rec.interim = true
        rec.addEventListener("result", on_start)
    }
    rec.start()
}
function stopped() {
    grabar.style.display = "flex";
    detener.style.display = "none";
    rec.stop()
}

function processed_text(text_p) {
    //Tratamiento del ejercicio
    var token = $("[name='csrfmiddlewaretoken']").attr("value");
    var idexer = exercise.pk
    let loqs = false
    let number;
    let sub_text;
    let cont = 0;
    screen_text = exercise.fields.text;
    screen_text = screen_text.replace(/[.,:";¿?¡!]/gi, '')
    screen_text = screen_text.toLowerCase()
    let screen_text_list = screen_text.split(' ')
    text_p = text_p.toLowerCase()
    let text_p_list = text_p.split(' ')

    text_p_list.forEach((element, index) => {
        if (index === 0) {
            sub_text = screen_text_list.slice(index, (index + 2))
        } else if (index === (screen_text_list.length - 1)) {
            sub_text = screen_text_list.slice((index - 1), index + 1)
        } else {
            sub_text = screen_text_list.slice((index - 1), (index + 2))
        }
        if (sub_text.includes(element)) {
            cont++;
        }
    });

    number = Math.round((cont / screen_text_list.length) * 100)
    let score = (cont / screen_text_list.length) * exercise.fields.punctuation
    
    //Resultados del ejercicio
    if (number <= 50) {
        score = 0
        Swal.fire({
            title: '<strong>Tu resultado: </strong>',
            icon: 'error',
            html:
                `<div class="progress"  style="height: 30px;"><div class="progress-bar progress-bar-striped progress-bar-animated" style="width:${number}%">${number}%</div></div>` +
                `Ganaste: ${score.toFixed(2)}`,
            focusConfirm: false,
            confirmButtonText: 
                '<i class="fa fa-thumbs-up"></i> Inténtalo de nuevo!',
            confirmButtonAriaLabel: 'Thumbs up, great!',
            
        })
    }else{

        Swal.fire({
            title: '<strong>Tu resultado: </strong>',
            icon: 'success',
            html:
                `<div class="progress"  style="height: 30px;"><div class="progress-bar progress-bar-striped progress-bar-animated" style="width:${number}%">${number}%</div></div>` +
                `Ganaste: ${score.toFixed(2)}`,
            focusConfirm: false,
            confirmButtonText:
                '<i class="fa fa-thumbs-up"></i> Okey!',
            confirmButtonAriaLabel: 'Thumbs up, great!',
            preConfirm: () => {
                return fetch(`/polls/save/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': token,
                    },
                    body: JSON.stringify({
                        iduser: iduser,
                        idexer: idexer,
                        score: score,
                    })
                })
                    .then(response => {
                        if (!response.ok) {
                            console.log('Todo salió mal...')
                        }
                        console.log(response)
                        return response
                    })
                    .catch(error => {
                        Swal.showValidationMessage(
                            `Request failed: ${error}`
                        )
                    })
            }
        })
    } 
}