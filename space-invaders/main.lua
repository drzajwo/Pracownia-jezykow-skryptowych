-- PLAYER

player = {}
player.x = 100
player.y = 580

player.bullets = {}
player.bullets_generation_tick = 30
player.bullet_speed = 4
player_width = 50
player_height = 20


function player:shoot()
	if player.bullets_generation_tick <= 0 then
		player.bullets_generation_tick = 30
		bullet = {}
		bullet.x = player.x + (player_width / 2)
		bullet.y = 550
		table.insert(player.bullets, bullet)
		love.audio.play(player_shoot_sound)
	end
end

function player_movement_update()
	if love.keyboard.isDown('right') then
		if player.x > 750 then
			player.x = 750
		end
		player.x = player.x + 5
	end
	if love.keyboard.isDown('left') then
		if player.x  < 10 then
			player.x = 10
		end
		player.x = player.x - 5
	end
	if love.keyboard.isDown('space') then
		player.shoot()
	end
end

function detect_players_collisions()
	for i, bullet in pairs(enemies_list.bullets) do
		if bullet.y >= player.y - player_height and bullet.x > player.x and bullet.x < player.x + player_width then
			table.remove(enemies_list.bullets, i)
			love.audio.play(explode_sound)
			is_game_over = true
		end
	end
end

-- ENEMY

enemies_list = {}
enemies_list.enemies = {}
enemies_list.movement_tick = 260
enemies_list.bullets_generation_tick = 180
enemies_list.bullet_speed = 3
enemies_list.bullets = {}
enemy_width = 40
enemy_height = 20

function enemies_list:spawn_row(data)
	for i=0,5 do
		x = 120 * i + 100 + self.x_offset
		enemy = {}
		enemy.x = x
		enemy.y = self.y
		table.insert(enemies_list.enemies, enemy)
	end

end

function enemies_movement_update()
	if enemies_list.movement_tick <= 0 then
		enemies_list.movement_tick = 260
		for _, enemy in pairs(enemies_list.enemies) do
			enemy.y = enemy.y + 10
		end
	end
end

function enemies_list:shoot()
	if enemies_list.bullets_generation_tick <= 0 and next(enemies_list.enemies) ~= nil then
		enemies_list.bullets_generation_tick = 180
		random_enemy = enemies_list.enemies[math.random(#enemies_list.enemies)]
		bullet = {}
		bullet.x = random_enemy.x + (enemy_width / 2)
		bullet.y = random_enemy.y
		table.insert(enemies_list.bullets, bullet)
		love.audio.play(enemy_shoot_sound)
	end
end

function detect_enemies_collisions()
	for i, enemy in pairs(enemies_list.enemies) do
		for j, bullet in pairs(player.bullets) do
			if bullet.y <= enemy.y + enemy_height and bullet.x > enemy.x and bullet.x < enemy.x + enemy_width then
				table.remove(enemies_list.enemies, i)
				table.remove(player.bullets, j)
				love.audio.play(explode_sound)
			end
		end
	end
end

-- LOVE

is_game_over = false
is_won = false

function love.load()
	player.image = love.graphics.newImage('images/player.png')
	player_shoot_sound = love.audio.newSource('sounds/shoot.mp3','static')
	enemy_shoot_sound = love.audio.newSource('sounds/enemy_shoot.mp3','static')
	explode_sound = love.audio.newSource('sounds/explode.mp3','static')
	enemies_list.image = love.graphics.newImage('images/invader.png')
	enemies_list.spawn_row{y = 0,x_offset = -40}
	enemies_list.spawn_row{y = 30,x_offset = 0}
	enemies_list.spawn_row{y = 60,x_offset = 40}
	enemies_list.spawn_row{y = 90,x_offset = 0}
	music = love.audio.newSource('sounds/music.mp3','static')
	music:setLooping(true)
	-- TODO: uncomment
	-- love.audio.play(music)
end

function love.draw()
	if is_game_over then
		love.graphics.setColor(1,0,0)
		love.graphics.print("GAME OVER!", 200, 300)
	elseif is_won then
		love.graphics.setColor(0,1,0)
		love.graphics.print("YOU WON!", 200, 300)
	else
		love.graphics.setColor(1,1,1)
		for it, bullet in pairs(player.bullets) do
		love.graphics.rectangle("fill",bullet.x, bullet.y, 5,10)
		end
		love.graphics.setColor(1,0,0)
		for it, bullet in pairs(enemies_list.bullets) do
		love.graphics.rectangle("fill",bullet.x, bullet.y, 5,10)
		end
		love.graphics.setColor(1,1,1)
		for _, enemy in pairs(enemies_list.enemies) do
			love.graphics.draw(enemies_list.image, enemy.x, enemy.y, 0, 1)
		end
		love.graphics.draw(player.image, player.x, 580, 0, 1)
	end
end

function update_game_conditions()
	player_movement_update()
	enemies_movement_update()
	-- player bullets
	for it, bullet in pairs(player.bullets) do
		bullet.y = bullet.y - player.bullet_speed
		if bullet.y < 0 then
			table.remove(player.bullets, it)
		end
	end
	-- enemies shooting
	enemies_list.shoot()
	for it, bullet in pairs(enemies_list.bullets) do
		bullet.y = bullet.y + enemies_list.bullet_speed
		if bullet.y > 600 then
			table.remove(enemies_list.bullets, it)
		end
	end

	-- collisions
	detect_enemies_collisions()
	detect_players_collisions()

	-- ticks update
	player.bullets_generation_tick = player.bullets_generation_tick - 1
	enemies_list.movement_tick = enemies_list.movement_tick - 1 
	enemies_list.bullets_generation_tick =  enemies_list.bullets_generation_tick - 1
end

function love.update()
	if love.keyboard.isDown('q') then
		love.event.quit()
	end
	if next(enemies_list.enemies) == nil then
		is_won = true
	end
	if not is_game_over and not is_won then
		update_game_conditions()
	end
end
