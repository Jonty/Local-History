<?php

    // This exists entirely because the port the API is using is blocked from the
    // Guardian offices and I can't be bothered with mod_proxy.
    
    $data = file("http://localhost:8910/?lat={$_GET['lat']}&lon={$_GET['lon']}");
    print $data[0];
