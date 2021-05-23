let orientation: CompassDirection = EAST
// Helper methods
function moveAgentByTeleport(direction: SixDirection, amount: number) {
    const currentPosition = agent.getPosition()
    let newPosition: Position = pos(0, 0, 0)

    switch (direction) {
        case UP:
            newPosition = positions.add(currentPosition, pos(0, amount, 0))
            break;
        case DOWN:
            newPosition = positions.add(currentPosition, pos(0, -amount, 0))
            break;
        case RIGHT:
            if (orientation === NORTH) {
                newPosition = positions.add(currentPosition, pos(amount, 0, 0))
            } else if (orientation === SOUTH) {
                 newPosition = positions.add(currentPosition, pos(-amount, 0, 0))
            } else if (orientation === EAST) {
                newPosition = positions.add(currentPosition, pos(0, 0, amount))
            } else if (orientation === WEST) {
                newPosition = positions.add(currentPosition, pos(0, 0, -amount))
            }
            break;
        case LEFT:
            if (orientation === NORTH) {
                newPosition = positions.add(currentPosition, pos(-amount, 0, 0))
            } else if (orientation === SOUTH) {
                 newPosition = positions.add(currentPosition, pos(amount, 0, 0))
            } else if (orientation === EAST) {
                newPosition = positions.add(currentPosition, pos(0, 0, -amount))
            } else if (orientation === WEST) {
                newPosition = positions.add(currentPosition, pos(0, 0, amount))
            }
            break;
        case FORWARD:
            if (orientation === NORTH) {
                newPosition = positions.add(currentPosition, pos(0, 0, -amount))
            } else if (orientation === SOUTH) {
                newPosition = positions.add(currentPosition, pos(0, 0, amount))
            } else if (orientation === EAST) {
                newPosition = positions.add(currentPosition, pos(amount, 0, 0))
            } else if (orientation === WEST) {
                newPosition = positions.add(currentPosition, pos(-amount, 0, 0))
            }
            break;
        case BACK:
            if (orientation === NORTH) {
                newPosition = positions.add(currentPosition, pos(0, 0, amount))
            } else if (orientation === SOUTH) {
                newPosition = positions.add(currentPosition, pos(0, 0, -amount))
            } else if (orientation === EAST) {
                newPosition = positions.add(currentPosition, pos(-amount, 0, 0))
            } else if (orientation === WEST) {
                newPosition = positions.add(currentPosition, pos(amount, 0, 0))
            }
            break;
    }
    agent.teleport(newPosition, orientation)
}

function toggleOrientation () {
    switch (orientation) {
        case NORTH:
            orientation = SOUTH
            break
        case SOUTH:
            orientation = NORTH
            break
        case EAST:
            orientation = WEST
            break
        case WEST:
            orientation = EAST
            break
    }
}

function setOrientation (direction: number) {
    switch (direction) {
        case 0:
            orientation = NORTH
            break
        case 1:
            orientation = EAST
            break
        case 2:
            orientation = SOUTH
            break
        case 3:
            orientation = WEST
            break
        default:
            orientation = NORTH
    }
}

// Building methods

function buildBase (height: number, width: number) {
    for (let index = 0; index < height; index++) {
        for (let index = 0; index < 4; index++) {
            agent.setItem(COBBLESTONE, 64, 1)
            agent.move(FORWARD, width)
            agent.turn(LEFT_TURN)
        }
        agent.move(UP, 1)
    }
}

function buildFence (width: number, length: number) {
    const startPositon = agent.getPosition()
    // const moveDir = orientation === NORTH || orientation === SOUTH ? LEFT : RIGHT
    const moveDir = LEFT
    for (let index = 0; index <= 1; index++) {
        agent.teleport(startPositon, orientation)
        moveAgentByTeleport(UP, 1)
        moveAgentByTeleport(moveDir, index * width)
        agent.setItem(COBBLESTONE_WALL, 64, 1)
        agent.move(FORWARD, length)
    }
}

function buildBridgePlatform (width: number, length: number) {
    const startPositon = agent.getPosition()
    const moveDir = LEFT
    for (let index = 0; index <= width; index++) {
        agent.teleport(startPositon, orientation)
        moveAgentByTeleport(moveDir, index)
        agent.setItem(COBBLESTONE, 64, 1)
        agent.move(FORWARD, length)
    }
}

function buildStairsFence (height: number, placeTorch: boolean) {
    agent.setItem(COBBLESTONE, 64, 1)
    agent.move(UP, height)
    if (placeTorch) {
        agent.setItem(TORCH, 64, 1)
        agent.move(UP, 1)
        moveAgentByTeleport(DOWN, 1)
    }
}

function buildStairs (height: number, width: number) {
    const startPositon = agent.getPosition()
    for (let index = 0; index <= height; index++) {
        agent.teleport(startPositon, orientation)
        moveAgentByTeleport(BACK, index+1)
        moveAgentByTeleport(DOWN, index)
        const isTorchNeeded = index === 0 || index === height
        buildStairsFence(3, isTorchNeeded)
        agent.setItem(COBBLESTONE_STAIRS, 64, 1)
        moveAgentByTeleport(LEFT, 1)
        moveAgentByTeleport(DOWN, 3)
        agent.move(LEFT, width - 1)
        buildStairsFence(3, isTorchNeeded)
    }
}

// direction:
// 0 - NORTH
// 1 - EAST
// 2 - SOUTH
// 3 - WEST
player.onChat("bridge", function (height: number, length: number, direction: number) {
    const width = 4
    setOrientation(direction)
    agent.teleportToPlayer()
    moveAgentByTeleport(FORWARD, 1)
    agent.setSlot(1)
    agent.setAssist(PLACE_ON_MOVE, true)
    agent.setAssist(DESTROY_OBSTACLES, true)

    // build first base with stairs
    buildBase(height, width)
    const firstBasePositon = agent.getPosition()
    agent.teleport(firstBasePositon, orientation)
    buildStairs(height, width)

    // build platform connecting bases and fence
    agent.teleport(firstBasePositon, orientation)
    buildBridgePlatform(width, length)
    agent.teleport(firstBasePositon, orientation)
    buildFence(width, length)

    // build second base with stairs
    agent.teleport(firstBasePositon, orientation)
    moveAgentByTeleport(FORWARD, length - width -1)
    moveAgentByTeleport(DOWN, height)
    buildBase(height, width)
    moveAgentByTeleport(UP, 1)
    agent.place(DOWN)
    moveAgentByTeleport(DOWN, 1)
    moveAgentByTeleport(FORWARD, width)
    moveAgentByTeleport(LEFT, width)
    toggleOrientation()
    buildStairs(height, width)
    toggleOrientation()
    moveAgentByTeleport(FORWARD, 5)
})
