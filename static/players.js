function sendRoomCode()
{
    var room_code = document.getElementById('roomcode').value
    //alert( room_code ) //DEBUG
    console.log(room_code)
    const request = new XMLHttpRequest()
    request.open('POST', `/update_list/${room_code}`)
    request.send();
}

function update_list()
{
    let roomcode = document.getElementById('roomcode').value
    let player_div = document.querySelector('#players');
    fetch(`/update_list/${roomcode}`).then(
        response => response.json()
    ).then(
        data => {
            document.getElementById('players').innerHTML="";
            for( player of data )
            {
                console.log( player );
                document.getElementById('players').innerHTML+="<tr><td>"+ player +"</td></tr>";
            }
        }
    );
}

setInterval( update_list, 1000 );
