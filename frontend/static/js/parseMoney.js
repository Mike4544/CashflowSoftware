function toMoney(val) {
    val = parseFloat(val).toFixed(2);

    if(val < 1000) {
        return val;
    }
    if(val < 1000000) {
        return (val/1000).toFixed(2) + " Mii";
    }
    if(val < 1000000000) {
        return (val/1000000).toFixed(2) + " Mil";
    }
    else {
        return (val/1000000000).toFixed(2) + " Miliarde";
    }

    return val;
}