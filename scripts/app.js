Vue.config.devtools = true

var app = new Vue({
    el: "#app",
    data() {
        return {
            connectedBolts: [],
            selectedBolt: '',
        }
    },
    methods: {
        async connectBolt() {

            bolt = new SpheroBolt();
            await bolt.connect();
            if (bolt.connected) {
                console.log(bolt);
                // console.log("Connected with BOLT");
                this.connectedBolts.push({ botID: bolt });
                bolt.setMainLedColor(255, 255, 255);
                bolt.setBackLedColor(255, 0, 0);
                const listLength = this.connectedBolts.length;

                switch (true) {
                    case (listLength <= 26):
                        let ascii = String.fromCharCode((listLength + 64));
                        bolt.printChar(ascii, 255, 255, 255);
                        this.connectedBolts[listLength - 1].botName = (ascii + ' Wit');
                        break;

                    case (listLength <= 52):
                        ascii = String.fromCharCode(((listLength -= 26) + 64));
                        bolt.printChar(ascii, 255, 0, 0);
                        this.connectedBolts[listLength - 1].botName = (ascii + ' Rood');
                        break;

                    case (listLength <= 78):
                        ascii = String.fromCharCode(((listLength -= 52) + 64));
                        bolt.printChar(ascii, 0, 255, 0);
                        this.connectedBolts[listLength - 1].botName = (ascii + ' Groen');
                        break;

                    case (listLength <= 104):
                        ascii = String.fromCharCode(((listLength -= 78) + 64));
                        bolt.printChar(ascii, 0, 0, 255);
                        this.connectedBolts[listLength - 1].botName = (ascii + ' Blauw');
                        break;
                }
                
                bolt.on("onWillSleepAsync", () => {
                    console.log('Waking up robot');
                    bolt.wake();
                });
                // console.log(this.connectedBolts)
            }
        },

        // Home made function
        setColor(bolt, red, green, blue) {
            bolt.setMatrixColor(red, green, blue);
        },
        setColorToAll(red, green, blue) {
            for (let i = 0; i < this.connectedBolts.length; i++) {
                // console.log("KLEUR AANGEPAST BOLT")
                this.setColor(this.connectedBolts[i].botID, 0, 255, 0);
            }
        },
        goForwardToAll(speed) {
            for (let i = 0; i < this.connectedBolts.length; i++) {
                console.log("Go forward all");
                this.connectedBolts[i].botID.roll(speed, 0, []);
            }
        },
        calibrateAll() {
            for (let i = 0; i < this.connectedBolts.length; i++) {
                console.log("Calibrate all!");
                this.connectedBolts[i].botID.calibrateToNorth();
            }
        },
        collorOne() {
            console.log(this.selectedBolt.botID)
            this.setColor(this.selectedBolt.botID, 0, 0, 255);
        },
        rotateBolt() {
            console.log(this.selectedBolt)
            this.selectedBolt.botID.setHeading(45);
        }
    }
})
