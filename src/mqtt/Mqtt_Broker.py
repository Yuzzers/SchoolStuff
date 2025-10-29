import asyncio, threading, time
from amqtt.broker import Broker
from amqtt.plugins.base import BasePlugin
from src.colors import Colors


class MQTTBroker:
    def __init__(self, host="127.0.0.1", port=1883, allow_anonymous=True):
        self.host = host
        self.port = port
        self.allow_anonymous = allow_anonymous
        self._broker = None
        self._loop = None
        self._thread = None
        self.running = False

    def _make_config(self):
        return {
            "listeners": {
                "default": {
                    "type": "tcp",
                    "bind": f"{self.host}:{self.port}",
                }
            },
            "plugins": ["amqtt.plugins.authentication.AnonymousAuthPlugin",],
        }

    async def _start_broker(self):
        self._broker = Broker(self._make_config())
        await self._broker.start()

    def start(self, background=True):
        """Start the MQTT broker. If background=True, runs in a thread."""
        def run():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            try:
                self._loop.run_until_complete(self._start_broker())
                self._loop.run_forever()
            except Exception as e:
                print(f"Broker error: {e}")
            finally:
                self._loop.run_until_complete(self._broker.shutdown())
        
        self.running = True
        if background:
            self._thread = threading.Thread(target=run, daemon=True)
            self._thread.start()
        else:
            run()
        
    def wait_until_running(self):
        print(f"\n{Colors.yellow}* waiting for broker{Colors.reset}")
        start = time.time()
        while True:
            if self.running:
                break
            if time.time() - start >= 5:
                raise TimeoutError(f"Condition {name} not met within {timeout} seconds")
            time.sleep(interval)
        print(f"{Colors.green}* broker is ready {Colors.reset}")
        

    def close(self):
        """Stop the broker."""
        if not self.running:
            return
        self.running = False
        if self._loop and self._broker:
            asyncio.run_coroutine_threadsafe(self._broker.shutdown(), self._loop)
            self._loop.call_soon_threadsafe(self._loop.stop)
        print("MQTT broker stopped.")


if __name__ == "__main__":
    broker = MQTTBroker(host="127.0.0.1", port=1883)
    try:
        broker.start(background=False)  # blocking
    except KeyboardInterrupt:
        print("\nBroker interrupted by user.")
    finally:
        broker.close()
