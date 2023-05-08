function flash_msg()
{
    var error = document.getElementById('flash_msg').value

    if( error == null )
    {}
    else if( error == "username" )
    {
        alert( "username already taken!" );
    }

    else if( error == "roomcode" )
    {
        alert( "roomcode already generated.. this was a 1 in 106387358923716524807713475752456393740167855629859291136 chance...\ngo buy a lottery ticket... and let me know this actually happened" );
    }

    else if( error == "room" )
    {
        alert( "that lobby does not exist!" );
    }

    else if( error == "full" )
    {
        alert( "that lobby is full!" );
    }

    else if( error == "error" )
    {
        alert( "an undefined error occured" );
    }
}
