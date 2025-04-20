const express =require("express")
const multer =require("multer");
const bodyParser=require("body-parser")
const cors = require("cors");
const app= express();
const storage=multer.diskStorage({
    destination:(req,res,cb)=>{
        cb(null,"uploads/")
    },
    filename:(req,file,cb)=>{
        cb(null ,Date.now()+"_"+file.originalname)
    }
});//this return the storage engine and we are using diskstorage engine to gain more access of uploaded to change its name and destination
const uploads=multer({storage})
app.use(cors());//?
app.use(bodyParser.text());
app.use(express.static("uploads"));//?
app.use(express.static("compressed"));//?
app.get("/",(req,res)=>{
    res.sendFile(__dirname+"/index.html")
})
app.post("/uploads",uploads.single("file"),(req,res)=>{
    console.log("file has been uploaded")
    const fs=require("fs");
    const filepath=req.file.path;
    const originalname=req.file.originalname;
    fs.readFile(filepath,"utf-8",(err,data)=>{
        if(err)
        {
            res.json({
                message:"error reading a file"
            })
        }  
        let count=1;
        let compressed="";
        for(let i=1;i<=data.length;i++)
        {
            if(data[i-1]==data[i])
            {
                count++;
            }
            else
            {
                compressed=compressed +data[i-1]+count
                count=1;
            }
        }
        const filename = `${Date.now()}_compressed_${originalname}`;
        const compressedfilepath= `compressed/${filename}`
        fs.writeFile(compressedfilepath,compressed,(err)=>{
            if(err)
            {
                return res.json({
                    message:"error"
                })
            }
            else{
                res.json({
                    message:"successful",
                    downloadLink: `http://localhost:3000/${filename}`
                })
            }
        })
    })
})
app.get('/compress',(req,res)=>{
    let input=req.headers.input;
    if(!input)
    {
        res.json({
            message:"file not found"
        })
    }
    else
    {
        let count=1;
        compressed="";
        for(let i=1;i<=input.length;i++)
        {
            if(input[i-1]==input[i])
            {
                count++;
            }
            else
            {
                compressed=compressed +input[i-1]+count
                count=1;
            }
        }
        res.send(compressed)
    }
})
app.get("/decompress",(req,res)=>{
    let input=req.headers.input;
    if(!input)
    {
        res.json({
            msg:"nothing to decompress"
        })
    }
    else{
        let decompress=""
        for(let i =0;i<input.length;)
        {
            let numstr=""
            let char=input[i];
            i++;
            while(i<input.length && !isNaN(input[i]))
            {
                numstr=numstr+input[i];
                i++;
            }
            let count= parseInt(numstr);
            for(let j=0;j<count;j++)
            {
                decompress=decompress+char;
            }
        }
        res.send(decompress)
    }
})

app.listen(3000)
