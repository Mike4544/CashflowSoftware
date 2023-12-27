function toMoney(val) {
    neg = val < 0;
    val = parseFloat(Math.abs(val)).toFixed(2);

    if(val < 1000) {
        return val * (neg ? -1 : 1);
    }
    if(val < 1000000) {
        return (val/1000).toFixed(2) * (neg ? -1 : 1) + " Mii";
    }
    if(val < 1000000000) {
        return (val/1000000).toFixed(2) * (neg ? -1 : 1) + " Mil";
    }
    else {
        return (val/1000000000).toFixed(2) * (neg ? -1 : 1) + " Miliarde";
    }

    return val * (neg ? -1 : 1);
}