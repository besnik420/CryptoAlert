const element = document.querySelector('.bn-table-tbody');
if (element) {	
    var outputString = "";
    for (let i = 1; i <= element.childElementCount; i++) {
        var content = element.childNodes[i]; 
        if(content){       
			var traderName ="";
			var traderWinRate = "";
			var classNameIndicator = "";
            var coinTypeIndicator = "";
			var entryPriceIndicator = "";
			
		//trader name
            traderName = document.querySelector(".translation-nickname").innerText;
            outputString += " " + traderName;

		// short or long 
            classNameIndicator = content.childNodes[0].childNodes[0].classList[0];
            if(classNameIndicator == "css-2cibqf"){
                //red
                outputString +=" " + "short";
            }else{
				//green
                outputString +=" " + "long";
            }
			                
        // coin type            
			classNameIndicator = content.childNodes[0].childNodes[0].childNodes[0].innerText.split("\n")[0];
            outputString +=  " " + classNameIndicator;			
        
		// entry price
			entryPriceIndicator = content.childNodes[2].textContent;
            outputString += " " + entryPriceIndicator;

            //outputString += " %";  
            if(i != element.childElementCount-1){
                     outputString += "\n";  
            }		
        }
    }
}
return outputString;