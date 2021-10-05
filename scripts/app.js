Vue.config.devtools = true;
ascii = Array.from(Array(26)).map((e, i) => i + 65);
alphabet = ascii.map((x) => String.fromCharCode(x));
colors = ['White']; // add more colors to support more than 26 bolts

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


var app = new Vue({
    el: "#app",
    data() {
        return {
            connectedBolts: [],
            selectedBolt: '',
            possible_Combinations: colors.flatMap(d => alphabet.map(v => d + ' ' + v)),
            rotateValue: 0,
        }
    },
    methods: {
        async vierkant() {
            //let bolts = this.connectedBolts.slice(1, 3);
            let bolts = this.connectedBolts
            console.log("VIERKANT!")

            bolts[1].roll(50, 0, []);
            bolts[2].roll(50, 0, []);
            await sleep(5000);

            bolts[1].roll(50, 0, []);
            bolts[2].roll(50, 0, []);
            await sleep(5000);
            bolts[1].roll(50, 0, []);
            bolts[2].roll(50, 0, []);

            console.log("go forward");
            await sleep(5000);
            console.log("Rotate")
            bolts[1].roll(30, 270, []);
            bolts[2].roll(30, 90, []);
        },
        async connectBolt() {
            bolt = new SpheroBolt();
            await bolt.connect();
            if (bolt.connected) {
                console.log(bolt);
                this.connectedBolts.push(bolt);
                this.boltAssignLetterColor(bolt);
                this.boltPrintChar(bolt);
                bolt.setMainLedColor(255, 255, 255);
                bolt.setBackLedColor(255, 0, 0);

                // console.log("Connected with BOLT");
                // this.connectedBolts.push({ botID: bolt });

                bolt.on("onWillSleepAsync", () => {
                    this.wakeAllBolts()
                });

                bolt.on("onCompassNotify", async (angle) => {
                    bolt.setHeading(angle);
                    for (let i = 0; i < this.connectedBolts.length; i++) {
                        this.boltPrintChar(this.connectedBolts[i])
                    }
                });
                // this.connectedBolts[0].botID.configureSensorStream()
                // console.log(this.connectedBolts)
            }
        },
        // Home made function for testing
        setColor(bolt, red, green, blue) {
            bolt.setMatrixColor(red, green, blue);
        },
        setColorToAll(red, green, blue) {
            for (let i = 0; i < this.connectedBolts.length; i++) {
                // console.log("KLEUR AANGEPAST BOLT")
                this.setColor(this.connectedBolts[i], 0, 255, 0);
            }
        },
        goForwardToAll(speed) {
            for (let i = 0; i < this.connectedBolts.length; i++) {
                console.log("Go forward all");
                this.connectedBolts[i].roll(speed, 0, []);
            }
        },
        rotateAllBolts() {
            for (let i = 0; i < this.connectedBolts.length; i++) {
                console.log("Rotate all");
                this.connectedBolts[i].setHeading(180);
            }
        },
        calibrateAll() {
            for (let i = 0; i < this.connectedBolts.length; i++) {
                console.log("Calibrate all!");
                this.connectedBolts[i].calibrateToNorth();
            }
        },
        collorOne() {
            console.log(this.selectedBolt)
            this.setColor(this.selectedBolt, 0, 0, 255);
        },
        rotateBolt() {
            console.log(this.selectedBolt)
            this.selectedBolt.setHeading(this.rotateValue);
        },
        wakeAllBolts() {
            console.log('Waking up robot');
            for (let i = 0; i < this.connectedBolts.length; i++) {
                this.connectedBolts[i].wake();
            }
        },
        disconnectBolt() {
            console.log(this.selectedBolt.name + ' ' + this.selectedBolt.color + ' bolt disconnected');
            this.selectedBolt.disconnect();
            const colorLetter = (this.selectedBolt.color + ' ' + this.selectedBolt.name);
            this.possible_Combinations.push(colorLetter);
            this.possible_Combinations.sort();
            this.connectedBolts.splice((this.connectedBolts.indexOf(this.selectedBolt)), 1);
        },
        boltAssignLetterColor(bolt) {
            let colorLetter = this.possible_Combinations.splice(0, 1);
            colorLetter = colorLetter[0].split(' ');
            bolt.name = colorLetter[1];
            bolt.color = colorLetter[0];
        },
        boltPrintChar(bolt) {
            switch (bolt.color) {
                case ('Blue'):
                    bolt.printChar(bolt.name, 0, 100, 255);
                    break;

                case ('Green'):
                    bolt.printChar(bolt.name, 0, 255, 0);
                    break;

                case ('Red'):
                    bolt.printChar(bolt.name, 255, 0, 0);
                    break;

                case ('White'):
                    bolt.printChar(bolt.name, 255, 255, 255);
                    break;
            }
        },
    },
});

// Garbage collection
delete ascii
delete alphabet
delete colors
