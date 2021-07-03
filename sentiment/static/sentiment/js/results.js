function saveBlob(blob,fileName) {
  var a = document.createElement("a");
  document.body.appendChild(a);
  a.style = "display: none";
  var url = window.URL.createObjectURL(blob);
  a.href = url;
  a.download = fileName;
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
};

function export_csv(data){
          data = data.replaceAll("Timestamp","new Date").replaceAll(", tz='tzutc()'","")
          data = data.replaceAll(/(\r\n|\n|\r)/gm, "");
          data = eval(data)
          data = typeof data != 'object' ? JSON.parse(data) : data;
          var strData = "Tweet Id,Created Time,Processed Tweet,Subjectivity,Polarity,Sentiment,Analysis Value" + '\r\n';
          for (var i = 0; i < data.length; i++) {
            var line = '';
            for (var index in data[i]) {
              if(index == "raw_tweet"){
                continue;
              }
                line += data[i][index];
                line += ','
            }

            strData += line + '\r\n';
        }
          

       const blob = new Blob([strData], {type: 'text/csv'});
       var fileName = "tweets.csv";
       saveBlob(blob,fileName);
}

function export_pdf(id){
  var id_List = ["sentiment-chart", "timeline-chart-5minutes", "timeline-chart-10minutes", 
                "timeline-chart-15minutes", "hashtag", "subject-chart"]
  var svgIdList = ["positive-word-tags", "negative-word-tags", "neutral-word-tags"]
  var opt = {
    filename:     id+'.pdf',
    html2canvas:  { logging: true, scale:1 },
    jsPDF:        { unit: 'pt', format: 'a4', putOnlyUsedFonts:true, orientation: 'landscape' }
  };

  if(id){
    var element = document.getElementById(id)
    html2pdf().set(opt).from(element).save();
  }
  else{
    opt.filename = "Result Report.pdf"
    var element = document.getElementById(id_List[0])
    let doc = html2pdf().set(opt).from(element).toPdf()

    for (let j = 0; j < svgIdList.length; j++) {
      element = document.getElementById(svgIdList[j])
      var svgElement = element.getElementsByTagName("svg");
      svgElement[0].setAttribute("x", svgElement[0].x.baseVal.value);
      svgElement[0].setAttribute("y", svgElement[0].y.baseVal.value);
      svgElement[0].setAttribute("width", svgElement[0].width.baseVal.value);
      svgElement[0].setAttribute("height", svgElement[0].height.baseVal.value);
      doc = doc.get('pdf').then(
        pdf => { pdf.addPage() }
      ).from(element).toContainer().toCanvas().toPdf()
    }
     
    for (let j = 1; j < id_List.length; j++) {
        element = document.getElementById(id_List[j])
        doc = doc.get('pdf').then(
          pdf => { pdf.addPage() }
        ).from(element).toContainer().toCanvas().toPdf()
    }
    function addFooters() {
      const pageCount = doc.internal.getNumberOfPages();
      for(var i = 0; i < pageCount; i++) {
          doc.text(String(i),196,285);
      }
    }
    addFooters()
    doc.save()
  } 
}

window.onload = function(){
  document.getElementById("loading").style.display = "none";
  document.getElementById("content").style.display = "block";
}