

function copyToClipboardAsLink(nameId, pathId, asPicture) {
    let name = document.getElementById(nameId).innerHTML;
    let path = document.getElementById(pathId).innerHTML;
    let text = "[" + name + "](" + path +")";
    if (asPicture) {
        text = "!" + text
    }
    navigator.clipboard.writeText(text);
}
