void setup(){
  Serial.begin(9600);
  pinMode(13,OUTPUT);
}


void loop(){
  while (Serial.available()>0){
    char c = Serial.read();
    
//    if(c=='y'){
//      digitalWrite(13,HIGH);
//    }
//    else if(c=='n'){
//      digitalWrite(13,LOW);
//    }    
//    
    
    
    if(c=='1'){
      digitalWrite(13,HIGH);
      //digitalWrite(13,LOW);
    }   
    
    
    else if(c=='2'){
     
    }
    
    
    else if(c=='3'){
      
      
    }
  }
}
