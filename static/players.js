function sendRoomCode()
{
    var room_code = document.getElementById('title').value
    alert( room_code )
    console.log(room_code)
    const request = new XMLHttpRequest()
    request.open('POST', `/update_list/${JSON.stringify(room_code)}`)
    request.send();
}

function update_list()
{
    let roomcode = document.getElementById('title').value
    let player_div = document.querySelector('#players');
    fetch(`/update_list/${JSON.stringify(roomcode)}`).then(
        response => response.json()
    ).then(
        data => {
            document.getElementById('players').innerHTML=data;
        }
    );
}

setInterval( update_list, 1000 );
